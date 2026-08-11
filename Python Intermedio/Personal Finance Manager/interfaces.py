import FreeSimpleGUI as sg

from persistence import (
    save_categories,
    save_movements,
)


def get_table_values(manager):
    table_values = []

    for movement in manager.movements:
        amount = movement.amount

        if movement.movement_type == "Expense":
            amount = -amount

        table_values.append(
            [
                movement.movement_type,
                movement.title,
                f"{amount:.2f}",
                movement.category,
            ]
        )

    return table_values


def save_all_data(manager):
    save_categories(manager.categories)
    save_movements(manager.movements)


def create_main_window(manager):
    headings = [
        "Type",
        "Title",
        "Amount",
        "Category",
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
        ],
        [
            sg.Table(
                values=get_table_values(manager),
                headings=headings,
                key="-TABLE-",
                auto_size_columns=True,
                justification="left",
                num_rows=15,
            )
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
                    values["-CATEGORY-NAME-"]
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
                )

                window.close()

                return True

            except ValueError as error:
                sg.popup_error(str(error))


def run_app(manager):
    window = create_main_window(manager)

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
                save_all_data(manager)

                window["-TABLE-"].update(
                    values=get_table_values(manager)
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
                save_all_data(manager)

                window["-TABLE-"].update(
                    values=get_table_values(manager)
                )

    window.close()