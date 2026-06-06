"""Phase 4.x.x — Extension & Sales Navigator."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from contact360_docgen import run_phase  # noqa: E402

if __name__ == "__main__":
    print(run_phase(4), "files")
