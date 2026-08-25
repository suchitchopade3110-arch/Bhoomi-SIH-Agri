"""
BHOOMI Master Validation Runner Shim
"""
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from rag.validation.run_full_rag_validation import run_full_master_validation

if __name__ == "__main__":
    run_full_master_validation()
