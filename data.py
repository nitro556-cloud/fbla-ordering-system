"""Menu data and JSON storage for the single-process, offline cafe demo."""
import json
import os
from pathlib import Path

MENU = [
    {'id': 1, 'name': 'Latte', 'category': 'Drinks', 'price': 459, 'stock': 50, 'image': 'latte.jpg'},
    {'id': 2, 'name': 'Espresso', 'category': 'Drinks', 'price': 359, 'stock': 75, 'image': 'espresso.jpg'},
    {'id': 3, 'name': 'Cold Brew', 'category': 'Drinks', 'price': 379, 'stock': 0, 'image': 'cold-brew.jpg'},
    {'id': 4, 'name': 'Iced Tea', 'category': 'Drinks', 'price': 299, 'stock': 20, 'image': 'iced-tea.jpg'},
    {'id': 5, 'name': 'Black Coffee', 'category': 'Drinks', 'price': 249, 'stock': 20, 'image': 'black-coffee.jpg'},
    {'id': 6, 'name': 'Blueberry Muffin', 'category': 'Food', 'price': 550, 'stock': 20, 'image': 'blueberry-muffin.jpg'},
    {'id': 7, 'name': 'Croissant', 'category': 'Food', 'price': 559, 'stock': 2, 'image': 'croissant.jpg'},
    {'id': 8, 'name': 'Caesar Salad', 'category': 'Food', 'price': 799, 'stock': 20, 'image': 'caesar-salad.jpg'},
    {'id': 9, 'name': 'Cinnamon Rolls', 'category': 'Food', 'price': 439, 'stock': 20, 'image': 'cinnamon-roll.jpg'},
]

# Tests can use a temporary file without changing the demonstration's orders.
DATA_FILE = Path(os.environ.get("CAFE_DATA_FILE", Path(__file__).with_name("cafe_data.json")))


def load_data():
    """Read saved orders and stock; return fresh menu data on the first run."""
    if not DATA_FILE.exists():
        return {"menu": [dict(item) for item in MENU], "orders": []}
    # Invalid storage raises an error instead of silently erasing sales history.
    with DATA_FILE.open(encoding="utf-8") as source:
        return json.load(source)


def save_data(state):
    """Save the supplied stock and orders together; return nothing."""
    temporary_file = DATA_FILE.with_suffix(".tmp")
    with temporary_file.open("w", encoding="utf-8") as destination:
        json.dump(state, destination, indent=2)
    # Replace only after the whole file is written, avoiding half-written JSON.
    temporary_file.replace(DATA_FILE)
