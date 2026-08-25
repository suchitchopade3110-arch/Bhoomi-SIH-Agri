"""
Roboflow Universe Open Rice Pest & Disease Adapter (SRC-DS-04)
Source: Roboflow Open Computer Vision Community
License: CC-BY 4.0 / CC0
"""
from pathlib import Path
from typing import Any, Dict, Generator, Tuple
from .base_adapter import BaseVisionSourceAdapter


class RoboflowRiceAdapter(BaseVisionSourceAdapter):
    def __init__(self):
        super().__init__(
            source_id="SRC-DS-04",
            dataset_name="Roboflow Universe Open Rice Pests",
            license_status="APPROVED_FOR_TRAINING",
            publisher="Roboflow Open Community"
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
                    "source_image_id": f"ROBOFLOW-{fpath.stem}",
                    "file_path": fpath,
                    "raw_label": raw_label,
                    "original_filename": fpath.name,
                    "source_url": "https://universe.roboflow.com/search?q=rice+pest",
                    "download_url": "https://universe.roboflow.com/",
                    "license": "CC-BY 4.0",
                    "license_status": self.license_status,
                    "publisher": self.publisher
                }

    def attempt_download(self, target_raw_dir: Path) -> Tuple[bool, str]:
        # Roboflow Universe requires user API key for programmatic bulk download export.
        return False, "DOWNLOAD_BLOCKED_EXTERNAL_ACCESS: Roboflow API key required for bulk zip export download."
