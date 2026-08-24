"""
PlantVillage Rice Collection Adapter (SRC-DS-02)
Source: Penn State University / Hughes & Salathe
License: CC-BY-NC-SA 4.0 (Approved for Research Training)
"""
from pathlib import Path
from typing import Any, Dict, Generator, Tuple
from .base_adapter import BaseVisionSourceAdapter


class PlantVillageRiceAdapter(BaseVisionSourceAdapter):
    def __init__(self):
        super().__init__(
            source_id="SRC-DS-02",
            dataset_name="PlantVillage Rice Collection",
            license_status="APPROVED_FOR_TRAINING",
            publisher="Penn State University / Hughes & Salathe"
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
                    "source_image_id": f"PLANTVIL-{fpath.stem}",
                    "file_path": fpath,
                    "raw_label": raw_label,
                    "original_filename": fpath.name,
                    "source_url": "https://plantvillage.psu.edu/",
                    "download_url": "https://github.com/spMohanty/PlantVillage-Dataset",
                    "license": "CC-BY-NC-SA 4.0",
                    "license_status": self.license_status,
                    "publisher": self.publisher
                }

    def attempt_download(self, target_raw_dir: Path) -> Tuple[bool, str]:
        # Standard PlantVillage repository lacks native rice images (focuses on tomato/potato/apple)
        return False, "DOWNLOAD_BLOCKED_EXTERNAL_ACCESS: Main PlantVillage GitHub repository does not contain native Oryza sativa sub-trees."
