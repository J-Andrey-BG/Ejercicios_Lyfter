def validate_category_name(name):
    cleaned_name = name.strip()

    if not cleaned_name:
        raise ValueError("Category name cannot be empty.")

    return cleaned_name


def validate_title(title):
    cleaned_title = title.strip()

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