import re
from datetime import date, datetime


DATE_FORMAT = "%d/%m/%Y"
DEFAULT_CATEGORY_COLOR = "#FFFFFF"


def get_today_string():
    return date.today().strftime(DATE_FORMAT)


def clean_text(value):
    if value is None:
        return ""

    return str(value).strip()


def validate_category_name(name):
    cleaned_name = clean_text(name)

    if not cleaned_name:
        raise ValueError("Category name cannot be empty.")

    return cleaned_name


def validate_title(title):
    cleaned_title = clean_text(title)

    if not cleaned_title:
        raise ValueError("Title cannot be empty.")

    return cleaned_title


def validate_amount(amount):
    try:
        number = float(amount)
    except (TypeError, ValueError):
        raise ValueError("Amount must be a valid number.")

    if number <= 0:
        raise ValueError("Amount must be greater than zero.")

    return number


def validate_movement_type(movement_type):
    if movement_type not in ("Income", "Expense"):
        raise ValueError("Movement type must be Income or Expense.")

    return movement_type


def validate_color(color):
    cleaned_color = clean_text(color)

    if not cleaned_color:
        return DEFAULT_CATEGORY_COLOR

    if not re.fullmatch(r"#[0-9a-fA-F]{6}", cleaned_color):
        raise ValueError("Color must be a valid hex color, for example #FFA500.")

    return cleaned_color.upper()


def parse_date_string(date_string):
    cleaned_date = clean_text(date_string)

    if not cleaned_date:
        raise ValueError("Date cannot be empty.")

    if not re.fullmatch(r"\d{2}/\d{2}/\d{4}", cleaned_date):
        raise ValueError("Invalid date format. Use dd/mm/yyyy.")

    try:
        return datetime.strptime(cleaned_date, DATE_FORMAT).date()
    except ValueError:
        raise ValueError("Invalid date format. Use dd/mm/yyyy.")


def validate_date_string(date_string, allow_future=False):
    parsed_date = parse_date_string(date_string)

    if not allow_future and parsed_date > date.today():
        raise ValueError("Date cannot be in the future.")

    return parsed_date.strftime(DATE_FORMAT)


def validate_date_range(start_date, end_date):
    parsed_start_date = parse_date_string(start_date)
    parsed_end_date = parse_date_string(end_date)

    if parsed_start_date > parsed_end_date:
        raise ValueError("Start date cannot be after end date.")

    return parsed_start_date, parsed_end_date