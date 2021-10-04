# file that stores the shared seed value
import pathlib
import os

seed_val_file = "seed_val.txt"
current_file_path = pathlib.Path(__file__).parent.resolve()
save_path = os.path.join(current_file_path, seed_val_file)


def save_seed(val, filename=save_path):
    """saves val. Called once in simulation1.py"""
    with open(filename, "w") as f:
        f.write(str(val))


def load_seed(filename=save_path):
    """loads val. Called by all scripts that need the shared seed value"""
    with open(filename, "rb") as f:
        return int(f.read())