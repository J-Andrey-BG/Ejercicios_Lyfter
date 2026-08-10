# Personal Finance Manager

This is a simple desktop application made with **Python** and **FreeSimpleGUI**.

The program allows the user to:

* Create categories.
* Add income.
* Add expenses.
* Show all movements in a table.
* Save the information automatically.
* Load the saved information when the program opens again.

---

## How It Works

The application uses categories before adding income or expenses.

Example categories:

* Food
* Work
* Transport
* Entertainment

After creating at least one category, the user can add:

* An income, such as salary.
* An expense, such as food or transportation.

All movements are displayed in the main table.

Expenses are shown as negative numbers in the table, but the user must enter the amount as a positive number.

For example:

```text
Expense: Pizza
Amount entered: 8500
Amount shown: -8500.00
```

The program saves the information in JSON files inside the `data` folder.

When the program is opened again, it loads the previous data automatically.

---

## Project Files

```text
personal_finance_manager/
│
├── main.py
├── models.py
├── logic.py
├── validations.py
├── persistence.py
├── interfaces.py
├── requirements.txt
│
├── data/
│
└── tests/
    └── test_logic.py
```

---

## Installation

First, open a terminal inside the project folder.

Then install the required libraries:

```bash
python -m pip install -r requirements.txt
```

The `requirements.txt` file must contain:

```text
FreeSimpleGUI
pytest
```

---

## Run the Application

To start the program, run:

```bash
python main.py
```

---

## Run the Tests

To run the unit tests, use:

```bash
python -m pytest
```

The tests check the main logic of the program without opening the graphical interface.

---

## Important Notes

The user must create at least one category before adding income or expenses.

If there are no categories, the program shows an error message.

The application saves data automatically after valid changes and also when the program closes.
