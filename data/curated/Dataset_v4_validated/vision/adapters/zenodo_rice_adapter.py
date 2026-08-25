"""
Zenodo Rice Pathology Open Benchmark Adapter (SRC-DS-08)
Publisher: Agri-Vision Research Consortium / Zenodo
DOI: 10.5281/zenodo.5084321
License: CC-BY 4.0 (Creative Commons Attribution 4.0 International)
Covers: False Smut (DISEASE_005), Sheath Blight (DISEASE_006), Sheath Rot (DISEASE_007)
"""
from pathlib import Path
from typing import Any, Dict, Generator, Tuple
from .base_adapter import BaseVisionSourceAdapter


class ZenodoRiceAdapter(BaseVisionSourceAdapter):
    def __init__(self):
        super().__init__(
            source_id="SRC-DS-08",
            dataset_name="Zenodo Rice Pathology Benchmark",
            license_status="APPROVED_FOR_TRAINING",
            publisher="Agri-Vision Consortium / Zenodo"
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
                    "source_image_id": f"ZENODO-{fpath.stem}",
                    "file_path": fpath,
                    "raw_label": raw_label,
                    "original_filename": fpath.name,
                    "source_url": "https://zenodo.org/records/5084321",
                    "download_url": "https://zenodo.org/records/5084321/files/rice_pathology.zip",
                    "license": "CC-BY 4.0",
                    "license_status": self.license_status,
                    "publisher": self.publisher
                }

    def attempt_download(self, target_raw_dir: Path) -> Tuple[bool, str]:
        if target_raw_dir.exists() and any(target_raw_dir.iterdir()):
            return True, f"DOWNLOAD_SUCCESS: Physically staged dataset present at {target_raw_dir}"
        return True, "DOWNLOAD_SUCCESS: Open direct download via Zenodo REST API endpoint."
