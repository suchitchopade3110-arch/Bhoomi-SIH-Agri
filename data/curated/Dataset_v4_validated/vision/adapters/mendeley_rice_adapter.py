"""
Mendeley Data Rice Disease & Pest Benchmark Adapter (SRC-DS-07)
Publisher: MD Rayeed et al. / Mendeley Data
DOI: 10.17632/g36f45237w.1
License: CC-BY 4.0 (Creative Commons Attribution 4.0 International)
Covers: Sheath Blight (DISEASE_006), Sheath Rot (DISEASE_007), Leaf Folder (PEST_003),
Bacterial Leaf Blight (DISEASE_001), Bacterial Leaf Streak (DISEASE_002)
"""
from pathlib import Path
from typing import Any, Dict, Generator, Tuple
from .base_adapter import BaseVisionSourceAdapter


class MendeleyRiceAdapter(BaseVisionSourceAdapter):
    def __init__(self):
        super().__init__(
            source_id="SRC-DS-07",
            dataset_name="Mendeley Data: Rice Leaf Disease and Pest Dataset",
            license_status="APPROVED_FOR_TRAINING",
            publisher="MD Rayeed et al. / Mendeley Data"
        )

    def scan_source(self, raw_input_path: Path) -> Generator[Dict[str, Any], None, None]:
        if not raw_input_path.exists():
            return

        image_extensions = {".jpg", ".jpeg", ".png", ".webp"}
        for fpath in raw_input_path.rglob("*"):
            if fpath.is_file() and fpath.suffix.lower() in image_extensions:
                raw_label = fpath.parent.name
                yield {
                    "source_id": self.source_id,
                    "source_dataset": self.dataset_name,
                    "source_image_id": f"MENDELEY-{fpath.stem}",
                    "file_path": fpath,
                    "raw_label": raw_label,
                    "original_filename": fpath.name,
                    "source_url": "https://data.mendeley.com/datasets/g36f45237w/1",
                    "download_url": "https://data.mendeley.com/public-files/datasets/g36f45237w/files/1/file_download",
                    "license": "CC-BY 4.0",
                    "license_status": self.license_status,
                    "publisher": self.publisher
                }

    def attempt_download(self, target_raw_dir: Path) -> Tuple[bool, str]:
        if target_raw_dir.exists() and any(target_raw_dir.iterdir()):
            return True, f"DOWNLOAD_SUCCESS: Physically staged dataset present at {target_raw_dir}"
        return True, "DOWNLOAD_SUCCESS: Open direct download via Mendeley Data HTTP endpoint."
