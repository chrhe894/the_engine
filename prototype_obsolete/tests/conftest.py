"""
Test configuration: make src/ importable and run from prototype root
so that scenarios/, simulations/, and cases/ resolve correctly.
"""

import sys
import os
from pathlib import Path

# Add src/ to the import path
PROTOTYPE_ROOT = Path(__file__).parent.parent
SRC = PROTOTYPE_ROOT / "src"
sys.path.insert(0, str(SRC))

# Run from prototype root so relative dirs (cases/, scenarios/) resolve
os.chdir(PROTOTYPE_ROOT)
