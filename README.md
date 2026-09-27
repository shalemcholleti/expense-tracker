# Expense Tracker CLI

A beginner-friendly terminal application for recording and understanding everyday spending in Indian rupees.

## Problem

Small purchases are easy to forget, making it difficult to know where money goes or how much has been spent over time.

## Solution

Expense Tracker provides a simple menu-driven command-line interface that stores expenses locally in a JSON file. Users can add, view, search, summarize, and delete records without needing a database or internet connection.

## Features

- Add an expense with amount, category, and description
- View all saved expenses in a readable table
- Search by category or description
- Calculate total spending
- Show spending grouped by category
- Delete an expense by its ID
- Automatically save data to `data/expenses.json`
- Validate amounts and required text fields

## Tech stack

- **Python 3.9+**
- Python standard library: `json`, `datetime`, `pathlib`
- Local JSON storage

## How to run

1. Clone the repository and open the project directory.
2. Make sure Python 3.9 or newer is installed.
3. Run:

   ```bash
   python3 src/expense_tracker.py
   ```

4. Select an option from the menu. Your data is saved automatically after adding or deleting an expense.

No third-party packages are required. The included `requirements.txt` is intentionally empty.

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
7. Exit

Choose an option: 1
Amount (₹): 450
Category: Food
Description: Lunch

Expense added successfully! (ID: 1)
```

## What I learned

- Using variables, input handling, and `if`/`elif`/`else` decisions
- Repeating a menu with loops
- Organizing records with lists and dictionaries
- Breaking a program into reusable functions
- Formatting strings for readable terminal output
- Reading and writing JSON files for simple persistence
- Validating user input and handling errors safely

## Future improvements

- Edit existing expenses
- Add date filters and monthly summaries
- Export data to CSV
- Add budgets and budget alerts
- Add automated tests and a richer terminal UI

## Project structure

```text
project/
├── README.md
├── src/
│   └── expense_tracker.py
├── data/
│   └── expenses.json
├── requirements.txt
└── .gitignore
```
