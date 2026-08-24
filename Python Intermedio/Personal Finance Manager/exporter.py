import csv
from pathlib import Path


def get_export_amount(movement):
    if movement.movement_type == "Expense":
        return -movement.amount

    return movement.amount


def export_movements_to_csv(manager, file_path):
    path = Path(file_path)

    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with path.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as file:
        writer = csv.writer(file)

        writer.writerow(
            [
                "Date",
                "Title",
                "Amount",
                "Category",
                "Type",
            ]
        )

        for movement in manager.movements:
            writer.writerow(
                [
                    movement.date,
                    movement.title,
                    f"{get_export_amount(movement):.2f}",
                    movement.category,
                    movement.movement_type,
                ]
            )

        writer.writerow([])
        writer.writerow(["Totals"])
        writer.writerow(["Total Income", f"{manager.get_total_income():.2f}"])
        writer.writerow(["Total Expenses", f"{manager.get_total_expenses():.2f}"])
        writer.writerow(["Net Balance", f"{manager.get_balance():.2f}"])

    return path