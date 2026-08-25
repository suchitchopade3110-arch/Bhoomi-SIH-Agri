"""
Base Adapter Interface for Vision Dataset Ingestion
"""
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Dict, Generator, Optional, Tuple


class BaseVisionSourceAdapter(ABC):
    def __init__(self, source_id: str, dataset_name: str, license_status: str, publisher: str):
        self.source_id = source_id
        self.dataset_name = dataset_name
        self.license_status = license_status
        self.publisher = publisher

    @abstractmethod
    def scan_source(self, raw_input_path: Path) -> Generator[Dict[str, Any], None, None]:
        """
        Yields raw image candidate records from a local raw input folder or extracted archive.
        Record format:
        {
            "source_image_id": str,
            "file_path": Path,
            "raw_label": str,
            "original_filename": str,
            "source_url": Optional[str],
            "download_url": Optional[str],
            "license": str,
            "license_status": str,
            "publisher": str
        }
        """
        pass

    @abstractmethod
    def attempt_download(self, target_raw_dir: Path) -> Tuple[bool, str]:
        """
        Attempts automated physical download of external dataset.
        Returns: (success: bool, status_message: str)
        """
        pass
