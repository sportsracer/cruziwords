import random
from pathlib import Path


def find_examples() -> list[Path]:
    this_dir = Path(__file__).parent
    csv_files = list(this_dir.glob("*.csv"))
    return csv_files


def random_example() -> Path:
    examples = find_examples()
    return random.choice(examples)
