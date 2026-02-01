import os
from constants import RECORD_FILE

def load_record() -> int:
    if os.path.exists(RECORD_FILE):
        try:
            with open(RECORD_FILE, "r") as f:
                return int(f.read().strip())
        except (ValueError, OSError):
            return 0
    return 0

def save_record(value: int):
    try:
        with open(RECORD_FILE, "w") as f:
            f.write(str(value))
    except OSError:
        pass