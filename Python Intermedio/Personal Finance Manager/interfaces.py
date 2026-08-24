import FreeSimpleGUI as sg

from exporter import export_movements_to_csv
from persistence import (
    save_categories,
    save_movements,
)
from validations import get_today_string


def get_display_amount(movement):
    if movement.movement_type == "Expense":
        return -movement.amount

    return movement.amount


def get_table_values(manager, movements=None):
    if movements is None:
        movements = manager.movements

    table_values = []

    for movement in movements:
        amount = get_display_amount(movement)

        table_values.append(
            [
                movement.date,
                movement.title,
                f"{amount:.2f}",
                movement.category,
                movement.movement_type,
            ]
        )

    return table_values


def get_table_row_colors(manager, movements=None):
    if movements is None:
        movements = manager.movements

    row_colors = []

    for index, movement in enumerate(movements):
        category_color = manager.get_category_color(movement.category)

        if category_color and category_color != "#FFFFFF":
            row_colors.append(
                (
                    index,
                    "black",
                    category_color,
                )
            )

    return row_colors


def save_all_data(manager):
    save_categories(manager.categories)
    save_movements(manager.movements)


def update_table(window, manager, movements=None):
    table_values = get_table_values(
        manager,
        movements,
    )

    row_colors = get_table_row_colors(
        manager,
        movements,
    )

    window["-TABLE-"].update(
        values=table_values,
        row_colors=row_colors,
    )


def update_totals(window, manager):
    window["-TOTAL-INCOME-"].update(
        f"Total Income: ₡{manager.get_total_income():.2f}"
    )

    window["-TOTAL-EXPENSES-"].update(
        f"Total Expenses: ₡{manager.get_total_expenses():.2f}"
    )

    window["-BALANCE-"].update(
        f"Balance: ₡{manager.get_balance():.2f}"
    )


def refresh_main_window(window, manager, movements=None):
    update_table(
        window,
        manager,
        movements,
    )

    update_totals(
        window,
        manager,
    )


def create_main_window(manager):
    headings = [
        "Date",
        "Title",
        "Amount",
        "Category",
        "Type",
    ]

    layout = [
        [
            sg.Text(
                "Personal Finance Manager",
                font=("Arial", 18),
            )
        ],
        [
            sg.Button("Add Category"),
            sg.Button("Add Expense"),
            sg.Button("Add Income"),
            sg.Button("Export to CSV"),
        ],
        [
            sg.Text("Start Date:"),
            sg.Input(
                key="-START-DATE-",
                size=(12, 1),
                tooltip="dd/mm/yyyy",
            ),
            sg.Text("End Date:"),
            sg.Input(
                key="-END-DATE-",
                size=(12, 1),
                tooltip="dd/mm/yyyy",
            ),
            sg.Button("Filter"),
            sg.Button("Clear Filter"),
        ],
        [
            sg.Table(
                values=get_table_values(manager),
                headings=headings,
                key="-TABLE-",
                auto_size_columns=True,
                justification="left",
                num_rows=15,
                row_colors=get_table_row_colors(manager),
            )
        ],
        [
            sg.Text(
                f"Total Income: ₡{manager.get_total_income():.2f}",
                key="-TOTAL-INCOME-",
                size=(25, 1),
            ),
            sg.Text(
                f"Total Expenses: ₡{manager.get_total_expenses():.2f}",
                key="-TOTAL-EXPENSES-",
                size=(25, 1),
            ),
            sg.Text(
                f"Balance: ₡{manager.get_balance():.2f}",
                key="-BALANCE-",
                size=(25, 1),
            ),
        ],
        [
            sg.Button("Exit")
        ],
    ]

    return sg.Window(
        "Personal Finance Manager",
        layout,
    )


def open_category_window(manager):
    layout = [
        [
            sg.Text("Category name:"),
            sg.Input(key="-CATEGORY-NAME-"),
        ],
        [
            sg.Text("Color:"),
            sg.Input(
                "#FFFFFF",
                key="-COLOR-",
                size=(10, 1),
            ),
            sg.ColorChooserButton(
                "Choose Color",
                target="-COLOR-",
            ),
        ],
        [
            sg.Button("Save"),
            sg.Button("Cancel"),
        ],
    ]

    window = sg.Window(
        "Add Category",
        layout,
        modal=True,
    )

    while True:
        event, values = window.read()

        if event in (
            sg.WIN_CLOSED,
            "Cancel",
        ):
            window.close()
            return False

        if event == "Save":
            try:
                manager.add_category(
                    values["-CATEGORY-NAME-"],
                    values["-COLOR-"],
                )

                window.close()

                return True

            except ValueError as error:
                sg.popup_error(str(error))


def open_movement_window(manager, movement_type):
    category_names = manager.get_category_names()

    layout = [
        [
            sg.Text("Title:"),
            sg.Input(key="-TITLE-"),
        ],
        [
            sg.Text("Amount:"),
            sg.Input(key="-AMOUNT-"),
        ],
        [
            sg.Text("Category:"),
            sg.Combo(
                category_names,
                key="-CATEGORY-",
                readonly=True,
            ),
        ],
        [
            sg.Text("Date:"),
            sg.Input(
                get_today_string(),
                key="-DATE-",
                size=(12, 1),
                tooltip="dd/mm/yyyy",
            ),
        ],
        [
            sg.Button("Save"),
            sg.Button("Cancel"),
        ],
    ]

    window = sg.Window(
        f"Add {movement_type}",
        layout,
        modal=True,
    )

    while True:
        event, values = window.read()

        if event in (
            sg.WIN_CLOSED,
            "Cancel",
        ):
            window.close()
            return False

        if event == "Save":
            try:
                manager.add_movement(
                    values["-TITLE-"],
                    values["-AMOUNT-"],
                    values["-CATEGORY-"],
                    movement_type,
                    values["-DATE-"],
                )

                window.close()

                return True

            except ValueError as error:
                sg.popup_error(str(error))


def export_data(manager):
    file_path = sg.popup_get_file(
        "Choose where to save the CSV file",
        save_as=True,
        no_window=True,
        default_extension=".csv",
        file_types=(
            ("CSV Files", "*.csv"),
        ),
    )

    if not file_path:
        return

    try:
        export_movements_to_csv(
            manager,
            file_path,
        )

        sg.popup(
            "Data exported successfully.",
            title="Export Complete",
        )

    except OSError as error:
        sg.popup_error(
            f"Could not export data: {error}"
        )


def run_app(manager):
    window = create_main_window(manager)

    current_filtered_movements = None

    while True:
        event, values = window.read()

        if event in (
            sg.WIN_CLOSED,
            "Exit",
        ):
            save_all_data(manager)

            break

        if event == "Add Category":
            category_added = open_category_window(
                manager
            )

            if category_added:
                save_all_data(manager)

        elif event == "Add Expense":
            if not manager.categories:
                sg.popup_error(
                    "You must create at least one "
                    "category before adding a movement."
                )

                continue

            movement_added = open_movement_window(
                manager,
                "Expense",
            )

            if movement_added:
                current_filtered_movements = None

                save_all_data(manager)

                window["-START-DATE-"].update("")
                window["-END-DATE-"].update("")

                refresh_main_window(
                    window,
                    manager,
                )

        elif event == "Add Income":
            if not manager.categories:
                sg.popup_error(
                    "You must create at least one "
                    "category before adding a movement."
                )

                continue

            movement_added = open_movement_window(
                manager,
                "Income",
            )

            if movement_added:
                current_filtered_movements = None

                save_all_data(manager)

                window["-START-DATE-"].update("")
                window["-END-DATE-"].update("")

                refresh_main_window(
                    window,
                    manager,
                )

        elif event == "Filter":
            try:
                current_filtered_movements = manager.filter_movements_by_date_range(
                    values["-START-DATE-"],
                    values["-END-DATE-"],
                )

                refresh_main_window(
                    window,
                    manager,
                    current_filtered_movements,
                )

            except ValueError as error:
                sg.popup_error(str(error))

        elif event == "Clear Filter":
            current_filtered_movements = None

            window["-START-DATE-"].update("")
            window["-END-DATE-"].update("")

            refresh_main_window(
                window,
                manager,
            )

        elif event == "Export to CSV":
            export_data(manager)

    window.close()