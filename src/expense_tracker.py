"""A small, persistent command-line expense tracker."""

from __future__ import annotations

import json
from datetime import date
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_FILE = PROJECT_ROOT / "data" / "expenses.json"


def load_expenses() -> list[dict[str, Any]]:
    """Load expenses from disk, returning an empty list when none exist."""
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    if not DATA_FILE.exists():
        return []

    try:
        with DATA_FILE.open("r", encoding="utf-8") as file:
            expenses = json.load(file)
    except (json.JSONDecodeError, OSError):
        print("Warning: Could not read saved expenses. Starting with an empty list.")
        return []

    return expenses if isinstance(expenses, list) else []


def save_expenses(expenses: list[dict[str, Any]]) -> None:
    """Save expenses to disk in a readable JSON format."""
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    with DATA_FILE.open("w", encoding="utf-8") as file:
        json.dump(expenses, file, indent=2, ensure_ascii=False)


def next_id(expenses: list[dict[str, Any]]) -> int:
    """Return the next available numeric expense ID."""
    return max((int(expense.get("id", 0)) for expense in expenses), default=0) + 1


def read_amount() -> float:
    """Read a positive expense amount from the user."""
    while True:
        raw_amount = input("Amount (₹): ").strip().replace(",", "")
        try:
            amount = float(raw_amount)
            if amount <= 0:
                raise ValueError
            return round(amount, 2)
        except ValueError:
            print("Please enter a positive number, for example 450 or 450.50.")


def add_expense(expenses: list[dict[str, Any]]) -> None:
    """Collect and save a new expense."""
    amount = read_amount()
    while True:
        category = input("Category: ").strip()
        if category:
            break
        print("Category cannot be empty.")

    while True:
        description = input("Description: ").strip()
        if description:
            break
        print("Description cannot be empty.")

    expense = {
        "id": next_id(expenses),
        "amount": amount,
        "category": category.title(),
        "description": description,
        "date": date.today().isoformat(),
    }
    expenses.append(expense)
    save_expenses(expenses)
    print(f"\nExpense added successfully! (ID: {expense['id']})")


def display_expenses(expenses: list[dict[str, Any]]) -> None:
    """Print expenses in a compact table."""
    if not expenses:
        print("\nNo expenses found.")
        return

    print("\nID   DATE         CATEGORY            DESCRIPTION                 AMOUNT")
    print("-" * 78)
    for expense in expenses:
        print(
            f"{expense['id']:<4} {expense['date']:<12} "
            f"{expense['category']:<19.19} {expense['description']:<27.27} "
            f"₹{expense['amount']:>8.2f}"
        )


def view_expenses(expenses: list[dict[str, Any]]) -> None:
    """Show every saved expense."""
    display_expenses(expenses)


def search_expenses(expenses: list[dict[str, Any]]) -> None:
    """Search descriptions and categories without case sensitivity."""
    query = input("Search by category or description: ").strip().lower()
    matches = [
        expense
        for expense in expenses
        if query in expense["category"].lower()
        or query in expense["description"].lower()
    ]
    print(f"\nFound {len(matches)} matching expense(s).")
    display_expenses(matches)


def show_total(expenses: list[dict[str, Any]]) -> None:
    """Print total spending across all expenses."""
    total = sum(float(expense["amount"]) for expense in expenses)
    print(f"\nTotal spending: ₹{total:.2f}")


def show_category_summary(expenses: list[dict[str, Any]]) -> None:
    """Print spending grouped by category."""
    totals: dict[str, float] = {}
    for expense in expenses:
        category = expense["category"]
        totals[category] = totals.get(category, 0) + float(expense["amount"])

    if not totals:
        print("\nNo expenses found.")
        return

    print("\nSPENDING BY CATEGORY")
    print("-" * 28)
    for category, amount in sorted(totals.items()):
        print(f"{category:<20} ₹{amount:>8.2f}")


def delete_expense(expenses: list[dict[str, Any]]) -> None:
    """Delete one expense by its ID."""
    if not expenses:
        print("\nNo expenses to delete.")
        return

    display_expenses(expenses)
    raw_id = input("\nEnter the expense ID to delete: ").strip()
    try:
        expense_id = int(raw_id)
    except ValueError:
        print("Please enter a valid numeric ID.")
        return

    for index, expense in enumerate(expenses):
        if expense["id"] == expense_id:
            removed = expenses.pop(index)
            save_expenses(expenses)
            print(f"Deleted expense #{expense_id}: {removed['description']}.")
            return

    print(f"No expense found with ID {expense_id}.")


def print_menu() -> None:
    """Print the main application menu."""
    print("\n===== EXPENSE TRACKER =====")
    print("1. Add Expense")
    print("2. View Expenses")
    print("3. Search Expense")
    print("4. Calculate Total Spending")
    print("5. Spending by Category")
    print("6. Delete Expense")
    print("7. Exit")


def main() -> None:
    """Run the interactive expense tracker."""
    expenses = load_expenses()
    actions = {
        "1": add_expense,
        "2": view_expenses,
        "3": search_expenses,
        "4": show_total,
        "5": show_category_summary,
        "6": delete_expense,
    }

    print("Welcome to Expense Tracker!")
    while True:
        print_menu()
        choice = input("Choose an option: ").strip()
        if choice == "7":
            print("Thank you for using Expense Tracker. Goodbye!")
            break
        action = actions.get(choice)
        if action:
            action(expenses)
        else:
            print("Invalid choice. Please select a number from 1 to 7.")


if __name__ == "__main__":
    main()
