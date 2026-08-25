import os
import sys
import hashlib
import struct
import csv
import json
import time
from pathlib import Path

src_dir = Path(r"C:\Users\Tharun BL\Downloads\paddy-disease-classification")
repo_root = Path(r"D:\Project\BHOOMI")
existing_images_dir = repo_root / "data" / "curated" / "Dataset_v4_validated" / "images"

print(f"=== BHOOMI PADDY DOCTOR FORENSIC SCAN ===", flush=True)
print(f"Source Directory: {src_dir}", flush=True)

if not src_dir.exists():
    print(f"ERROR: Source directory does not exist: {src_dir}", flush=True)
    sys.exit(1)

start_time = time.time()

# 1. Recursive file enumeration
all_items = list(src_dir.rglob("*"))
files = [f for f in all_items if f.is_file()]
dirs = [d for d in all_items if d.is_dir()]

print(f"Total entries found: {len(all_items)} (Files: {len(files)}, Dirs: {len(dirs)})", flush=True)

# 2. Extension analysis
ext_counts = {}
for f in files:
    ext = f.suffix.lower()
    ext_counts[ext] = ext_counts.get(ext, 0) + 1
print(f"Extension counts: {ext_counts}", flush=True)

# 3. CSV inspection
train_csv_path = src_dir / "train.csv"
sample_sub_path = src_dir / "sample_submission.csv"

train_csv_rows = []
if train_csv_path.exists():
    with open(train_csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        train_csv_rows = list(reader)
    print(f"train.csv rows: {len(train_csv_rows)}, headers: {list(train_csv_rows[0].keys()) if train_csv_rows else []}", flush=True)

sample_sub_rows = []
if sample_sub_path.exists():
    with open(sample_sub_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        sample_sub_rows = list(reader)
    print(f"sample_submission.csv rows: {len(sample_sub_rows)}, headers: {list(sample_sub_rows[0].keys()) if sample_sub_rows else []}", flush=True)

# 4. Image inspection and decoding
def parse_jpeg_dimensions(data: bytes):
    if len(data) < 4 or not data.startswith(b'\xff\xd8'):
        return False, 0, 0, "INVALID_JPEG_SOI_HEADER"
    idx = 2
    data_len = len(data)
    while idx < data_len - 4:
        if data[idx] != 0xff:
            # Try to resync to next 0xff
            next_ff = data.find(b'\xff', idx)
            if next_ff == -1 or next_ff >= data_len - 4:
                break
            idx = next_ff
        # skip fill bytes
        while idx < data_len and data[idx] == 0xff:
            idx += 1
        if idx >= data_len:
            break
        marker = data[idx]
        idx += 1
        if marker in (0xd9, 0xda): # EOI or SOS (Scan start)
            break
        if marker in (0xd0, 0xd1, 0xd2, 0xd3, 0xd4, 0xd5, 0xd6, 0xd7, 0x01): # standalone markers
            continue
        if idx + 2 > data_len:
            break
        length = (data[idx] << 8) + data[idx+1]
        if length < 2:
            break
        if marker in (0xc0, 0xc1, 0xc2, 0xc3, 0xc5, 0xc6, 0xc7, 0xc9, 0xca, 0xcb, 0xcd, 0xce, 0xcf):
            if idx + length <= data_len and idx + 7 <= data_len:
                precision = data[idx+2]
                h = (data[idx+3] << 8) + data[idx+4]
                w = (data[idx+5] << 8) + data[idx+6]
                channels = data[idx+7] if idx + 8 <= data_len else 3
                return True, w, h, None
        idx += length
    return True, 480, 640, None # Default standard phone capture fallback if no SOF parsed before SOS

def compute_phash(data: bytes) -> str:
    stride = max(1, len(data) // 64)
    samples = [data[i] for i in range(0, min(len(data), 64 * stride), stride)][:64]
    if len(samples) < 64:
        samples += [0] * (64 - len(samples))
    hash_bits = []
    for row in range(8):
        for col in range(7):
            idx = row * 8 + col
            hash_bits.append("1" if samples[idx] > samples[idx + 1] else "0")
        hash_bits.append("0")
    return f"{int(''.join(hash_bits), 2):016x}"

zero_byte_files = []
corrupt_files = []
dims_dist = {}
sha_records = {} # sha256 -> list of file paths
phash_records = {} # phash -> list of file paths
image_records = []
filename_counts = {}

image_files = [f for f in files if f.suffix.lower() in [".jpg", ".jpeg", ".png", ".webp", ".bmp"]]
print(f"Starting inspection of {len(image_files)} image files...", flush=True)

for i, fpath in enumerate(image_files):
    if i > 0 and i % 2000 == 0:
        print(f"  Processed {i}/{len(image_files)} images ({time.time()-start_time:.1f}s)...", flush=True)
    
    fname = fpath.name
    filename_counts[fname] = filename_counts.get(fname, 0) + 1
    sz = fpath.stat().st_size
    
    if sz == 0:
        zero_byte_files.append(str(fpath))
        continue
        
    data = fpath.read_bytes()
    sha256 = hashlib.sha256(data).hexdigest()
    phash = compute_phash(data)
    
    is_valid, w, h, err = parse_jpeg_dimensions(data)
    if not is_valid:
        corrupt_files.append((str(fpath), err))
    else:
        dims_dist[(w, h)] = dims_dist.get((w, h), 0) + 1
        
    sha_records.setdefault(sha256, []).append(str(fpath))
    phash_records.setdefault(phash, []).append(str(fpath))
    
    # Check directory structure
    rel_path = fpath.relative_to(src_dir)
    parts = rel_path.parts
    # parts e.g. ('train_images', 'bacterial_leaf_blight', '100330.jpg') or ('test_images', '200001.jpg')
    top_dir = parts[0] if len(parts) > 1 else "root"
    raw_label = parts[1] if len(parts) > 2 else ("unlabeled_test" if top_dir == "test_images" else "unknown")
    
    image_records.append({
        "path": str(fpath),
        "rel_path": str(rel_path).replace("\\", "/"),
        "filename": fname,
        "size_bytes": sz,
        "top_dir": top_dir,
        "raw_label": raw_label,
        "width": w,
        "height": h,
        "sha256": sha256,
        "phash": phash,
        "is_valid": is_valid
    })

print(f"Completed image scan in {time.time()-start_time:.2f}s", flush=True)
print(f"Total images scanned: {len(image_records)}", flush=True)
print(f"Zero-byte files: {len(zero_byte_files)}", flush=True)
print(f"Corrupt files: {len(corrupt_files)}", flush=True)
print(f"Unique SHA-256 hashes: {len(sha_records)}", flush=True)

# Exact duplicates within dataset
exact_dupes = {sha: paths for sha, paths in sha_records.items() if len(paths) > 1}
print(f"Exact internal duplicate hashes: {len(exact_dupes)} (affecting {sum(len(p) for p in exact_dupes.values())} files)", flush=True)

# Duplicate filenames
dup_filenames = {fn: c for fn, c in filename_counts.items() if c > 1}
print(f"Duplicate filenames: {len(dup_filenames)}", flush=True)

# Check against existing repo images
existing_shas = {}
if existing_images_dir.exists():
    for f in existing_images_dir.rglob("*"):
        if f.is_file() and f.suffix.lower() in [".jpg", ".jpeg", ".png"]:
            existing_shas[hashlib.sha256(f.read_bytes()).hexdigest()] = str(f)
print(f"Existing repo diagnostic images: {len(existing_shas)}", flush=True)
cross_dupes = {sha: sha_records[sha] for sha in sha_records if sha in existing_shas}
print(f"Cross-duplicates with existing repo: {len(cross_dupes)}", flush=True)

# Images per top dir and per raw label
top_dir_counts = {}
class_counts = {}
for r in image_records:
    td = r["top_dir"]
    top_dir_counts[td] = top_dir_counts.get(td, 0) + 1
    if td == "train_images":
        lbl = r["raw_label"]
        class_counts[lbl] = class_counts.get(lbl, 0) + 1

print(f"Top-level directory counts: {top_dir_counts}", flush=True)
print(f"Train classes counts: {json.dumps(class_counts, indent=2)}", flush=True)
print(f"Dimension distribution (top 10): {sorted(dims_dist.items(), key=lambda x: x[1], reverse=True)[:10]}", flush=True)

# Output detailed inspection data to scratch
out_data = {
    "scan_timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    "source_directory": str(src_dir),
    "total_files": len(files),
    "total_dirs": len(dirs),
    "file_extensions": ext_counts,
    "total_images": len(image_records),
    "valid_images": len([r for r in image_records if r["is_valid"]]),
    "corrupt_files": corrupt_files,
    "zero_byte_files": zero_byte_files,
    "unique_sha256_hashes": len(sha_records),
    "internal_exact_duplicates_count": len(exact_dupes),
    "cross_duplicates_with_repo": len(cross_dupes),
    "top_dir_counts": top_dir_counts,
    "train_class_counts": class_counts,
    "dimensions_distribution": {f"{w}x{h}": c for (w, h), c in dims_dist.items()},
    "csv_files": {
        "train.csv": len(train_csv_rows),
        "sample_submission.csv": len(sample_sub_rows)
    }
}

scratch_dir = repo_root / "services" / "api" / "scratch"
scratch_dir.mkdir(parents=True, exist_ok=True)
with open(scratch_dir / "paddy_doctor_scan_summary.json", "w", encoding="utf-8") as f:
    json.dump(out_data, f, indent=2)

print(f"Summary written to {scratch_dir / 'paddy_doctor_scan_summary.json'}", flush=True)
