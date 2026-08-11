import json
from pathlib import Path

from models import Category, Movement


BASE_DIR = Path(__file__).resolve().parent

DATA_DIR = BASE_DIR / "data"

CATEGORIES_FILE = DATA_DIR / "categories.json"
MOVEMENTS_FILE = DATA_DIR / "movements.json"


def load_categories(file_path=CATEGORIES_FILE):
    path = Path(file_path)

    if not path.exists():
        return []

    try:
        with path.open("r", encoding="utf-8") as file:
            data = json.load(file)

        return [
            Category.from_dict(item)
            for item in data
        ]

    except (
        OSError,
        json.JSONDecodeError,
        KeyError,
        TypeError,
    ):
        return []


def load_movements(file_path=MOVEMENTS_FILE):
    path = Path(file_path)

    if not path.exists():
        return []

    try:
        with path.open("r", encoding="utf-8") as file:
            data = json.load(file)

        return [
            Movement.from_dict(item)
            for item in data
        ]

    except (
        OSError,
        json.JSONDecodeError,
        KeyError,
        TypeError,
    ):
        return []


def save_categories(categories, file_path=CATEGORIES_FILE):
    path = Path(file_path)

    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    data = [
        category.to_dict()
        for category in categories
    ]

    with path.open(
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(
            data,
            file,
            indent=4,
            ensure_ascii=False,
        )


def save_movements(movements, file_path=MOVEMENTS_FILE):
    path = Path(file_path)

    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    data = [
        movement.to_dict()
        for movement in movements
    ]

    with path.open(
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(
            data,
            file,
            indent=4,
            ensure_ascii=False,
        )