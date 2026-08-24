from models import Category, Movement
from validations import (
    get_today_string,
    parse_date_string,
    validate_amount,
    validate_category_name,
    validate_color,
    validate_date_range,
    validate_date_string,
    validate_movement_type,
    validate_title,
)


class FinanceManager:
    def __init__(self, categories=None, movements=None):
        self.categories = categories if categories is not None else []
        self.movements = movements if movements is not None else []

    def add_category(self, name, color="#FFFFFF"):
        cleaned_name = validate_category_name(name)
        valid_color = validate_color(color)

        for category in self.categories:
            if category.name.lower() == cleaned_name.lower():
                raise ValueError("Category already exists.")

        category = Category(
            cleaned_name,
            valid_color,
        )

        self.categories.append(category)

        return category

    def add_movement(
        self,
        title,
        amount,
        category_name,
        movement_type,
        movement_date=None,
    ):
        if not self.categories:
            raise ValueError("No categories are available.")

        cleaned_title = validate_title(title)
        valid_amount = validate_amount(amount)
        valid_type = validate_movement_type(movement_type)

        cleaned_category_name = str(category_name).strip() if category_name else ""

        if not cleaned_category_name:
            raise ValueError("Please select a category.")

        category_exists = any(
            category.name == cleaned_category_name
            for category in self.categories
        )

        if not category_exists:
            raise ValueError("Selected category does not exist.")

        if movement_date is None:
            movement_date = get_today_string()

        valid_date = validate_date_string(
            movement_date,
            allow_future=False,
        )

        movement = Movement(
            cleaned_title,
            valid_amount,
            cleaned_category_name,
            valid_type,
            valid_date,
        )

        self.movements.append(movement)

        return movement

    def get_category_names(self):
        return [
            category.name
            for category in self.categories
        ]

    def get_category_color(self, category_name):
        for category in self.categories:
            if category.name == category_name:
                return category.color

        return "#FFFFFF"

    def get_total_income(self):
        return sum(
            movement.amount
            for movement in self.movements
            if movement.movement_type == "Income"
        )

    def get_total_expenses(self):
        return sum(
            movement.amount
            for movement in self.movements
            if movement.movement_type == "Expense"
        )

    def get_balance(self):
        return self.get_total_income() - self.get_total_expenses()

    def filter_movements_by_date_range(self, start_date, end_date):
        parsed_start_date, parsed_end_date = validate_date_range(
            start_date,
            end_date,
        )

        filtered_movements = []

        for movement in self.movements:
            movement_date = parse_date_string(movement.date)

            if parsed_start_date <= movement_date <= parsed_end_date:
                filtered_movements.append(movement)

        return filtered_movements