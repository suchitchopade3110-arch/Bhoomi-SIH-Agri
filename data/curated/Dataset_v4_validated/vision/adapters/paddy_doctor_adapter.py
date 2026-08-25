"""
Paddy Doctor Benchmark Adapter (SRC-DS-01)
Source: Makerere AI Lab / TNAU / AI4Good
License: CC-BY 4.0 (Approved for Training)
"""
from pathlib import Path
from typing import Any, Dict, Generator, Tuple
from .base_adapter import BaseVisionSourceAdapter


class PaddyDoctorAdapter(BaseVisionSourceAdapter):
    def __init__(self):
        super().__init__(
            source_id="SRC-DS-01",
            dataset_name="Paddy Doctor Benchmark",
            license_status="APPROVED_FOR_TRAINING",
            publisher="Makerere AI Lab / TNAU / AI4Good"
        )

    def scan_source(self, raw_input_path: Path) -> Generator[Dict[str, Any], None, None]:
        if not raw_input_path.exists():
            return

        image_extensions = {".jpg", ".jpeg", ".png", ".webp"}
        for fpath in raw_input_path.rglob("*"):
            if fpath.is_file() and fpath.suffix.lower() in image_extensions:
                # Paddy doctor folders are typically named after disease/pest (e.g., bacterial_leaf_blight/100001.jpg)
                raw_label = fpath.parent.name
                yield {
                    "source_id": self.source_id,
                    "source_dataset": self.dataset_name,
                    "source_image_id": f"PADDYDOC-{fpath.stem}",
                    "file_path": fpath,
                    "raw_label": raw_label,
                    "original_filename": fpath.name,
                    "source_url": "https://www.kaggle.com/competitions/paddy-disease-classification",
                    "download_url": "https://github.com/paddydoctor/paddy-doctor",
                    "license": "CC-BY 4.0",
                    "license_status": self.license_status,
                    "publisher": self.publisher
                }

    def attempt_download(self, target_raw_dir: Path) -> Tuple[bool, str]:
        # Check if dataset is physically present locally (e.g. user download)
        user_download_dir = Path(r"C:\Users\Tharun BL\Downloads\paddy-disease-classification")
        if user_download_dir.exists() and any(user_download_dir.iterdir()):
            return True, f"DOWNLOAD_SUCCESS: Physically downloaded dataset present at {user_download_dir}"
        if target_raw_dir.exists() and any(target_raw_dir.iterdir()):
            return True, f"DOWNLOAD_SUCCESS: Dataset present in local cache at {target_raw_dir}"
        # Kaggle competition datasets require Kaggle API token (~/.kaggle/kaggle.json)
        return False, "DOWNLOAD_BLOCKED_EXTERNAL_ACCESS: Kaggle API authentication credential required for bulk dataset download."
