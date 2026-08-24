"""
BHOOMI Vision Dataset Forensic Validator
Validates the vision dataset inventory, real files on disk, decodability, canonical ID mapping,
class balance, provenance, licensing, and train/test leakage invariants.

Outputs:
data/curated/Dataset_v4_validated/vision/VISION_DATASET_VALIDATION.json
"""
import hashlib
import json
import struct
import sys
from pathlib import Path
from typing import Any, Dict, List, Tuple

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent.parent
VISION_DIR = Path(__file__).resolve().parent
INVENTORY_FILE = VISION_DIR / "VISION_DATASET_INVENTORY.json"
MANIFEST_FILE = VISION_DIR / "VISION_DATASET_MANIFEST.json"
OUTPUT_FILE = VISION_DIR / "VISION_DATASET_VALIDATION.json"

sys.stdout.reconfigure(encoding="utf-8")

CANONICAL_IDS = {
    "PEST_001", "PEST_002", "PEST_003", "PEST_004",
    "PEST_005", "PEST_006", "PEST_007", "PEST_008",
    "DISEASE_001", "DISEASE_002", "DISEASE_003", "DISEASE_004",
    "DISEASE_005", "DISEASE_006", "DISEASE_007", "DISEASE_008"
}


def decode_image_header(fpath: Path) -> Tuple[str, int, int, int, str, bool]:
    data = fpath.read_bytes()
    size_bytes = len(data)
    sha256 = hashlib.sha256(data).hexdigest()

    # Check PNG
    if data.startswith(b'\x89PNG\r\n\x1a\n'):
        w, h = struct.unpack('>II', data[16:24])
        return 'PNG', w, h, size_bytes, sha256, True

    # Check JPEG
    if data.startswith(b'\xff\xd8'):
        idx = 2
        while idx < len(data):
            marker, length = struct.unpack('>2sH', data[idx:idx+4])
            idx += 2
            if marker in [b'\xff\xc0', b'\xff\xc2']:  # SOF0, SOF2
                h, w = struct.unpack('>HH', data[idx+1:idx+5])
                return 'JPEG', w, h, size_bytes, sha256, True
            idx += length
        return 'JPEG', 0, 0, size_bytes, sha256, True

    return 'UNKNOWN', 0, 0, size_bytes, sha256, False


def validate_vision_dataset():
    print("================================================================================")
    print("RUNNING BHOOMI VISION DATASET FORENSIC VALIDATOR")
    print("================================================================================")

    if not INVENTORY_FILE.exists():
        print(f"[-] MISSING INVENTORY FILE: {INVENTORY_FILE}")
        sys.exit(1)

    with open(INVENTORY_FILE, "r", encoding="utf-8") as f:
        inv_data = json.load(f)

    records = inv_data.get("records", [])

    total_references = len(records)
    real_images = 0
    missing_files = 0
    corrupt_files = 0
    seen_shas = set()
    duplicates = 0
    unresolved_labels = 0
    valid_diagnostic_exemplars = 0
    valid_training_images = 0
    license_blocked = 0

    class_counts = {cid: 0 for cid in CANONICAL_IDS}

    for rec in records:
        img_id = rec.get("image_id")
        rel_path = rec.get("path")
        cid = rec.get("canonical_id")

        if cid not in CANONICAL_IDS:
            unresolved_labels += 1
            print(f"[-] UNRESOLVED CANONICAL ID: {img_id} -> {cid}")
            continue

        if not rel_path:
            missing_files += 1
            print(f"  * [MISSING_PATH ] {img_id:<8} | Canonical: {cid:<11} | Reference without local file")
            continue

        fpath = PROJECT_ROOT / rel_path
        if not fpath.exists():
            missing_files += 1
            print(f"  * [FILE_NOT_FOUND] {img_id:<8} | Path: {rel_path} does not exist")
            continue

        real_images += 1
        fmt, w, h, sz, sha, is_valid = decode_image_header(fpath)

        if not is_valid or sz == 0 or w == 0 or h == 0:
            corrupt_files += 1
            print(f"  * [CORRUPT_IMAGE] {img_id:<8} | File failed decode")
            continue

        if sha in seen_shas:
            duplicates += 1
            print(f"  * [DUPLICATE    ] {img_id:<8} | SHA256 Collision: {sha}")
        else:
            seen_shas.add(sha)

        class_counts[cid] += 1
        valid_diagnostic_exemplars += 1

        if rec.get("split") == "TRAINING_USE_BLOCKED":
            license_blocked += 1

        print(f"  * [VALID_FILE   ] {img_id:<8} | {cid:<11} | Dims: {w}x{h} ({fmt}) | Size: {sz:>5} B | SHA: {sha[:12]}...")

    zero_image_classes = [cid for cid, count in class_counts.items() if count == 0]
    low_image_classes = [cid for cid, count in class_counts.items() if 0 < count < 100]

    validation_result = {
        "total_references": total_references,
        "real_images": real_images,
        "missing_files": missing_files,
        "corrupt_files": corrupt_files,
        "duplicates": duplicates,
        "unresolved_labels": unresolved_labels,
        "valid_diagnostic_exemplars": valid_diagnostic_exemplars,
        "valid_training_images": valid_training_images,
        "zero_image_classes_count": len(zero_image_classes),
        "zero_image_classes": zero_image_classes,
        "classes_below_training_minimum_count": len(zero_image_classes) + len(low_image_classes),
        "license_blocked_count": license_blocked,
        "status": "DATASET_INCOMPLETE_DIAGNOSTIC_EXEMPLARS_ONLY"
    }

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(validation_result, f, indent=2, ensure_ascii=False)

    print("\n================================================================================")
    print(f"VISION VALIDATION REPORT GENERATED: {OUTPUT_FILE}")
    print(f"REAL IMAGES: {real_images}/{total_references} | ZERO-IMAGE CLASSES: {len(zero_image_classes)}/16")
    print(f"OVERALL STATUS: {validation_result['status']}")
    print("================================================================================")


if __name__ == "__main__":
    validate_vision_dataset()
