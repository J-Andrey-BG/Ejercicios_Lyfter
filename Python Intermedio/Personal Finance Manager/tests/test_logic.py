from datetime import date, timedelta

import pytest

from exporter import export_movements_to_csv
from logic import FinanceManager
from persistence import (
    load_categories,
    load_movements,
    save_categories,
    save_movements,
)


def format_date(value):
    return value.strftime("%d/%m/%Y")


def test_add_valid_category_with_color():
    manager = FinanceManager()

    category = manager.add_category(
        "Food",
        "#FFA500",
    )

    assert category.name == "Food"
    assert category.color == "#FFA500"
    assert len(manager.categories) == 1


def test_reject_empty_category():
    manager = FinanceManager()

    with pytest.raises(ValueError):
        manager.add_category("   ")


def test_reject_duplicate_category():
    manager = FinanceManager()

    manager.add_category("Food")

    with pytest.raises(ValueError):
        manager.add_category("food")


def test_reject_invalid_color():
    manager = FinanceManager()

    with pytest.raises(ValueError):
        manager.add_category(
            "Food",
            "orange",
        )


def test_add_valid_income_with_date():
    manager = FinanceManager()

    today = format_date(date.today())

    manager.add_category("Work")

    movement = manager.add_movement(
        "Salary",
        "1000",
        "Work",
        "Income",
        today,
    )

    assert movement.title == "Salary"
    assert movement.amount == 1000.0
    assert movement.category == "Work"
    assert movement.movement_type == "Income"
    assert movement.date == today


def test_add_valid_expense_with_date():
    manager = FinanceManager()

    today = format_date(date.today())

    manager.add_category("Food")

    movement = manager.add_movement(
        "Lunch",
        "10.50",
        "Food",
        "Expense",
        today,
    )

    assert movement.movement_type == "Expense"
    assert movement.amount == 10.50
    assert movement.date == today


def test_reject_movement_without_categories():
    manager = FinanceManager()

    with pytest.raises(ValueError):
        manager.add_movement(
            "Salary",
            "1000",
            "Work",
            "Income",
            format_date(date.today()),
        )


def test_reject_empty_title():
    manager = FinanceManager()

    manager.add_category("Food")

    with pytest.raises(ValueError):
        manager.add_movement(
            "   ",
            "10",
            "Food",
            "Expense",
            format_date(date.today()),
        )


def test_reject_non_numeric_amount():
    manager = FinanceManager()

    manager.add_category("Food")

    with pytest.raises(ValueError):
        manager.add_movement(
            "Lunch",
            "abc",
            "Food",
            "Expense",
            format_date(date.today()),
        )


def test_reject_zero_amount():
    manager = FinanceManager()

    manager.add_category("Food")

    with pytest.raises(ValueError):
        manager.add_movement(
            "Lunch",
            "0",
            "Food",
            "Expense",
            format_date(date.today()),
        )


def test_reject_invalid_movement_type():
    manager = FinanceManager()

    manager.add_category("Food")

    with pytest.raises(ValueError):
        manager.add_movement(
            "Lunch",
            "10",
            "Food",
            "Transfer",
            format_date(date.today()),
        )


def test_reject_invalid_date_format():
    manager = FinanceManager()

    manager.add_category("Food")

    with pytest.raises(ValueError):
        manager.add_movement(
            "Lunch",
            "10",
            "Food",
            "Expense",
            "2025-07-20",
        )


def test_reject_nonexistent_date():
    manager = FinanceManager()

    manager.add_category("Food")

    with pytest.raises(ValueError):
        manager.add_movement(
            "Lunch",
            "10",
            "Food",
            "Expense",
            "31/02/2025",
        )


def test_reject_future_date():
    manager = FinanceManager()

    future_date = format_date(
        date.today() + timedelta(days=1)
    )

    manager.add_category("Food")

    with pytest.raises(ValueError):
        manager.add_movement(
            "Lunch",
            "10",
            "Food",
            "Expense",
            future_date,
        )


def test_calculate_totals_and_balance():
    manager = FinanceManager()

    today = format_date(date.today())

    manager.add_category("Work")
    manager.add_category("Food")

    manager.add_movement(
        "Salary",
        "1000",
        "Work",
        "Income",
        today,
    )

    manager.add_movement(
        "Lunch",
        "200",
        "Food",
        "Expense",
        today,
    )

    assert manager.get_total_income() == 1000.0
    assert manager.get_total_expenses() == 200.0
    assert manager.get_balance() == 800.0


def test_filter_movements_by_date_range():
    manager = FinanceManager()

    old_date = format_date(
        date.today() - timedelta(days=10)
    )

    recent_date = format_date(
        date.today() - timedelta(days=2)
    )

    start_date = format_date(
        date.today() - timedelta(days=5)
    )

    end_date = format_date(
        date.today()
    )

    manager.add_category("Food")

    manager.add_movement(
        "Old Expense",
        "10",
        "Food",
        "Expense",
        old_date,
    )

    manager.add_movement(
        "Recent Expense",
        "20",
        "Food",
        "Expense",
        recent_date,
    )

    filtered_movements = manager.filter_movements_by_date_range(
        start_date,
        end_date,
    )

    assert len(filtered_movements) == 1
    assert filtered_movements[0].title == "Recent Expense"


def test_reject_invalid_date_range():
    manager = FinanceManager()

    start_date = format_date(date.today())
    end_date = format_date(date.today() - timedelta(days=5))

    with pytest.raises(ValueError):
        manager.filter_movements_by_date_range(
            start_date,
            end_date,
        )


def test_save_and_load_data(tmp_path):
    manager = FinanceManager()

    today = format_date(date.today())

    manager.add_category(
        "Food",
        "#FFA500",
    )

    manager.add_movement(
        "Pizza",
        "8500",
        "Food",
        "Expense",
        today,
    )

    categories_file = tmp_path / "categories.json"
    movements_file = tmp_path / "movements.json"

    save_categories(
        manager.categories,
        categories_file,
    )

    save_movements(
        manager.movements,
        movements_file,
    )

    loaded_categories = load_categories(categories_file)
    loaded_movements = load_movements(movements_file)

    assert len(loaded_categories) == 1
    assert loaded_categories[0].name == "Food"
    assert loaded_categories[0].color == "#FFA500"

    assert len(loaded_movements) == 1
    assert loaded_movements[0].title == "Pizza"
    assert loaded_movements[0].date == today


def test_export_movements_to_csv(tmp_path):
    manager = FinanceManager()

    today = format_date(date.today())

    manager.add_category("Work")
    manager.add_category("Food")

    manager.add_movement(
        "Salary",
        "1200",
        "Work",
        "Income",
        today,
    )

    manager.add_movement(
        "Food",
        "100",
        "Food",
        "Expense",
        today,
    )

    csv_file = tmp_path / "export.csv"

    export_movements_to_csv(
        manager,
        csv_file,
    )

    content = csv_file.read_text(
        encoding="utf-8",
    )

    assert "Date,Title,Amount,Category,Type" in content
    assert "Salary" in content
    assert "Food" in content
    assert "Total Income" in content
    assert "Total Expenses" in content
    assert "Net Balance" in content