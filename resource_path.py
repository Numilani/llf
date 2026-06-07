import sys
import os

def is_frozen() -> bool:
    return True if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS") else False

def resource_path(path) -> str:
    if not is_frozen():
        return os.path.join(os.path.dirname(__file__), path)
    base = getattr(sys, "_MEIPASS", os.path.dirname(__file__))
    return os.path.join(base, path)
