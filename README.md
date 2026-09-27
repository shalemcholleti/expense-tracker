# Expense Tracker CLI

A beginner-friendly terminal application for recording and understanding everyday spending in Indian rupees.

## Problem

Small purchases are easy to forget, making it difficult to know where money goes or how much has been spent over time.

## Solution

Expense Tracker provides a simple menu-driven command-line interface that stores expenses locally in a JSON file. Users can add, view, search, summarize, edit, and delete records without needing a database or internet connection.

## Features

- Add an expense with amount, category, and description
- View all saved expenses in a readable table
- Search by category or description
- Calculate total spending
- Show spending grouped by category
- Edit an expense by ID, including amount, category, and description
- Show a filtered monthly summary using each expense's saved date
- Delete an expense by its ID
- Automatically save data to `data/expenses.json`
- Validate amounts and required text fields

## Tech stack

- **Python 3.9+**
- Python standard library: `json`, `datetime`, `pathlib`, `unittest`
- Local JSON storage

## How to run

1. Clone the repository and open the project directory.
2. Make sure Python 3.9 or newer is installed.
3. Run:

   ```bash
   python3 src/expense_tracker.py
   ```

4. Select an option from the menu. Your data is saved automatically after adding, editing, or deleting an expense.

No third-party packages are required. The included `requirements.txt` is intentionally empty.

## How to run tests

Run the automated test suite from the project root:

```bash
python3 -m unittest discover -s tests -v
```

The tests cover ID generation, total spending, category grouping, invalid amount retry handling, monthly filtering, and editing an expense.

## Screenshots

Example terminal session:

```text
===== EXPENSE TRACKER =====
1. Add Expense
2. View Expenses
3. Search Expense
4. Calculate Total Spending
5. Spending by Category
6. Delete Expense
7. Edit Expense
8. Monthly Summary
9. Exit

Choose an option: 7
Enter the expense ID to edit: 3
Current amount: ₹500.00
New amount (₹) [500.00]: 650
Current category: Food
New category [Food]: Restaurant
Current description: Lunch
New description [Lunch]: Dinner

Expense updated successfully.
```

Monthly summary example:

```text
===== MONTHLY SUMMARY =====
September 2026
Total spent: ₹12,450.00

Food         ₹4,200.00
Transport    ₹2,300.00
Shopping     ₹3,750.00
Other        ₹2,200.00
```

## What I learned

- Using variables, input handling, and `if`/`elif`/`else` decisions
- Repeating a menu with loops
- Organizing records with lists and dictionaries
- Modifying nested dictionaries inside a list
- Filtering records by a date condition
- Breaking a program into reusable functions
- Formatting strings for readable terminal output
- Reading and writing JSON files for simple persistence
- Writing automated tests with Python's `unittest` module
- Validating user input and handling errors safely

## Future improvements

- Export data to CSV
- Add budgets and budget alerts
- Add richer terminal colors and formatting

## Project structure

```text
project/
├── README.md
├── src/
│   ├── __init__.py
│   └── expense_tracker.py
├── tests/
│   └── test_expense_tracker.py
├── data/
│   └── expenses.json
├── requirements.txt
└── .gitignore
```
