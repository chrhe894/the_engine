"""
Shared bootstrap for entry-point scripts.

Ensures that data directories (cases/, scenarios/, simulations/) and the
.env file always resolve to the prototype root, regardless of the
directory the script was launched from.

Import this at the top of any runnable entry point:

    import _bootstrap  # noqa: F401
"""

import os
import sys
from pathlib import Path

# src/ is where the modules live; its parent is the prototype root.
_SRC = Path(__file__).resolve().parent
_PROTOTYPE_ROOT = _SRC.parent

# Make sibling modules importable even if launched oddly.
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

# Resolve data directories against the prototype root.
os.chdir(_PROTOTYPE_ROOT)

PROTOTYPE_ROOT = _PROTOTYPE_ROOT
