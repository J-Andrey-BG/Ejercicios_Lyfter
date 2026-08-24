# Personal Finance Manager

This is a simple desktop application made with **Python** and **FreeSimpleGUI**.

The program allows the user to manage personal income and expenses using a graphical interface.

---

## Features

The application allows the user to:

* Create categories.
* Assign a color to each category.
* Add income.
* Add expenses.
* Select a custom date for each movement.
* Show all movements in a table.
* Display category colors in the table.
* Filter movements by date range.
* Clear the active date filter.
* Show total income, total expenses, and balance.
* Export movements and totals to a CSV file.
* Save the information automatically.
* Load the saved information when the program opens again.

---

## How It Works

The user must create at least one category before adding income or expenses.

Example categories:

* Food
* Work
* Transport
* Entertainment

Each category can have a custom color.

After creating at least one category, the user can add:

* An income, such as salary.
* An expense, such as food or transportation.

Each movement includes:

* Date
* Title
* Amount
* Category
* Type

The required date format is:

```text
dd/mm/yyyy
```

Example:

```text
23/08/2026
```

The date cannot be in the future.

Expenses are shown as negative numbers in the table, but the user must enter the amount as a positive number.

Example:

```text
Expense: Pizza
Amount entered: 8500
Amount shown: -8500.00
```

The application also calculates:

* Total income
* Total expenses
* Net balance

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
├── exporter.py
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

## Data Storage

The application stores its internal data using JSON files.

The files are created inside the `data` folder:

```text
data/
├── categories.json
└── movements.json
```

Categories are saved with their name and color.

Movements are saved with their title, amount, category, type, and date.

---

## CSV Export

The application includes an `Export to CSV` button.

When the user exports the data, the generated CSV file includes:

* Date
* Title
* Amount
* Category
* Type
* Total income
* Total expenses
* Net balance

The CSV file is only used for exporting data.

The application still uses JSON files to save and load its internal data.

---

## Basic Usage

1. Run the application.

```bash
python main.py
```

2. Create a category.

Example:

```text
Category: Food
Color: #FFA500
```

3. Add an expense.

Example:

```text
Title: Pizza
Amount: 8500
Category: Food
Date: 23/08/2026
Type: Expense
```

4. Add an income.

Example:

```text
Title: Salary
Amount: 500000
Category: Work
Date: 23/08/2026
Type: Income
```

5. Use the date filter if you want to see only movements inside a specific date range.

Example:

```text
Start Date: 01/08/2026
End Date: 23/08/2026
```

6. Use `Clear Filter` to show all movements again.

7. Use `Export to CSV` to generate a CSV file with all movements and totals.

---

## Important Notes

The user must create at least one category before adding income or expenses.

If there are no categories, the program shows an error message.

Amounts must be positive numbers.

Dates must use this format:

```text
dd/mm/yyyy
```

Future dates are not allowed.

The application saves data automatically after valid changes and also when the program closes.

