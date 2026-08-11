from interfaces import run_app
from logic import FinanceManager
from persistence import (
    load_categories,
    load_movements,
)


def main():
    categories = load_categories()
    movements = load_movements()

    manager = FinanceManager(
        categories,
        movements,
    )

    run_app(manager)


if __name__ == "__main__":
    main()