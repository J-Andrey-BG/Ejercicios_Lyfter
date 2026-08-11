import pytest

from logic import FinanceManager


def test_add_valid_category():
    manager = FinanceManager()

    category = manager.add_category("Food")

    assert category.name == "Food"
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


def test_add_valid_income():
    manager = FinanceManager()

    manager.add_category("Work")

    movement = manager.add_movement(
        "Salary",
        "1000",
        "Work",
        "Income",
    )

    assert movement.title == "Salary"
    assert movement.amount == 1000.0
    assert movement.category == "Work"
    assert movement.movement_type == "Income"


def test_add_valid_expense():
    manager = FinanceManager()

    manager.add_category("Food")

    movement = manager.add_movement(
        "Lunch",
        "10.50",
        "Food",
        "Expense",
    )

    assert movement.movement_type == "Expense"
    assert movement.amount == 10.50


def test_reject_movement_without_categories():
    manager = FinanceManager()

    with pytest.raises(ValueError):
        manager.add_movement(
            "Salary",
            "1000",
            "Work",
            "Income",
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
        )