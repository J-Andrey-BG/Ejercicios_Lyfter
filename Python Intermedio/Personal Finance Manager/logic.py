from models import Category, Movement
from validations import (
    validate_amount,
    validate_category_name,
    validate_movement_type,
    validate_title,
)


class FinanceManager:
    def __init__(self, categories=None, movements=None):
        self.categories = categories if categories is not None else []
        self.movements = movements if movements is not None else []

    def add_category(self, name):
        cleaned_name = validate_category_name(name)

        for category in self.categories:
            if category.name.lower() == cleaned_name.lower():
                raise ValueError("Category already exists.")

        category = Category(cleaned_name)

        self.categories.append(category)

        return category

    def add_movement(self, title, amount, category_name, movement_type):
        if not self.categories:
            raise ValueError("No categories are available.")

        cleaned_title = validate_title(title)
        valid_amount = validate_amount(amount)
        valid_type = validate_movement_type(movement_type)

        category_exists = any(
            category.name == category_name
            for category in self.categories
        )

        if not category_exists:
            raise ValueError("Selected category does not exist.")

        movement = Movement(
            cleaned_title,
            valid_amount,
            category_name,
            valid_type,
        )

        self.movements.append(movement)

        return movement

    def get_category_names(self):
        return [
            category.name
            for category in self.categories
        ]