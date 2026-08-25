"""
PlantDoc Dataset Adapter (SRC-DS-03)
Source: IIT Delhi / University of Delhi
License: MIT / CC-BY 4.0 Compatible
"""
from pathlib import Path
from typing import Any, Dict, Generator, Tuple
from .base_adapter import BaseVisionSourceAdapter


class PlantDocAdapter(BaseVisionSourceAdapter):
    def __init__(self):
        super().__init__(
            source_id="SRC-DS-03",
            dataset_name="PlantDoc Field Benchmark",
            license_status="APPROVED_FOR_TRAINING",
            publisher="IIT Delhi / University of Delhi"
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
                    "source_image_id": f"PLANTDOC-{fpath.stem}",
                    "file_path": fpath,
                    "raw_label": raw_label,
                    "original_filename": fpath.name,
                    "source_url": "https://github.com/pratikkayal/PlantDoc-Dataset",
                    "download_url": "https://github.com/pratikkayal/PlantDoc-Dataset/archive/refs/heads/master.zip",
                    "license": "MIT / CC-BY 4.0 Compatible",
                    "license_status": self.license_status,
                    "publisher": self.publisher
                }

    def attempt_download(self, target_raw_dir: Path) -> Tuple[bool, str]:
        # PlantDoc public release contains 28 horticultural classes; rice is not present in official release.
        return False, "DOWNLOAD_BLOCKED_EXTERNAL_ACCESS: Official PlantDoc master release does not contain Oryza sativa classes."
