"""A small, persistent command-line expense tracker."""

from __future__ import annotations

import json
from datetime import date, datetime
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


def read_amount(prompt: str = "Amount (₹): ") -> float:
    """Read a positive expense amount from the user."""
    while True:
        raw_amount = input(prompt).strip().replace(",", "")
        try:
            amount = float(raw_amount)
            if amount <= 0:
                raise ValueError
            return round(amount, 2)
        except ValueError:
            print("Please enter a positive number, for example 450 or 450.50.")


def read_updated_amount(current_amount: float) -> float:
    """Read an updated amount, keeping the current value when left blank."""
    while True:
        raw_amount = input(f"New amount (₹) [{current_amount:.2f}]: ").strip().replace(",", "")
        if not raw_amount:
            return current_amount
        try:
            amount = float(raw_amount)
            if amount <= 0:
                raise ValueError
            return round(amount, 2)
        except ValueError:
            print("Please enter a positive number, or press Enter to keep the current amount.")


def read_updated_text(label: str, current_value: str) -> str:
    """Read updated text, keeping the current value when left blank."""
    updated_value = input(f"New {label} [{current_value}]: ").strip()
    return updated_value or current_value


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


def category_totals(expenses: list[dict[str, Any]]) -> dict[str, float]:
    """Return spending totals grouped by category."""
    totals: dict[str, float] = {}
    for expense in expenses:
        category = expense["category"]
        totals[category] = totals.get(category, 0) + float(expense["amount"])
    return totals


def show_category_summary(expenses: list[dict[str, Any]]) -> None:
    """Print spending grouped by category."""
    totals = category_totals(expenses)
    if not totals:
        print("\nNo expenses found.")
        return

    print("\nSPENDING BY CATEGORY")
    print("-" * 28)
    for category, amount in sorted(totals.items()):
        print(f"{category:<20} ₹{amount:>8.2f}")


def show_monthly_summary(expenses: list[dict[str, Any]], target_month: str | None = None) -> None:
    """Print total and category spending for a YYYY-MM month."""
    target_month = target_month or date.today().strftime("%Y-%m")
    try:
        month_label = datetime.strptime(target_month, "%Y-%m").strftime("%B %Y")
    except ValueError:
        print("Please use a month in YYYY-MM format.")
        return

    monthly_expenses = [
        expense for expense in expenses if expense.get("date", "").startswith(target_month)
    ]
    print("\n===== MONTHLY SUMMARY =====")
    print(month_label)
    if not monthly_expenses:
        print("No expenses found for this month.")
        return

    total = sum(float(expense["amount"]) for expense in monthly_expenses)
    print(f"Total spent: ₹{total:,.2f}\n")
    for category, amount in sorted(category_totals(monthly_expenses).items()):
        print(f"{category:<12} ₹{amount:,.2f}")


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


def edit_expense(expenses: list[dict[str, Any]]) -> None:
    """Update an existing expense's amount, category, and description."""
    if not expenses:
        print("\nNo expenses to edit.")
        return

    display_expenses(expenses)
    raw_id = input("\nEnter the expense ID to edit: ").strip()
    try:
        expense_id = int(raw_id)
    except ValueError:
        print("Please enter a valid numeric ID.")
        return

    expense = next((item for item in expenses if item["id"] == expense_id), None)
    if expense is None:
        print(f"No expense found with ID {expense_id}.")
        return

    print(f"\nCurrent amount: ₹{expense['amount']:.2f}")
    expense["amount"] = read_updated_amount(float(expense["amount"]))
    print(f"Current category: {expense['category']}")
    expense["category"] = read_updated_text("category", expense["category"]).title()
    print(f"Current description: {expense['description']}")
    expense["description"] = read_updated_text("description", expense["description"])
    save_expenses(expenses)
    print("\nExpense updated successfully.")


def print_menu() -> None:
    """Print the main application menu."""
    print("\n===== EXPENSE TRACKER =====")
    print("1. Add Expense")
    print("2. View Expenses")
    print("3. Search Expense")
    print("4. Calculate Total Spending")
    print("5. Spending by Category")
    print("6. Delete Expense")
    print("7. Edit Expense")
    print("8. Monthly Summary")
    print("9. Exit")


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
        "7": edit_expense,
        "8": show_monthly_summary,
    }

    print("Welcome to Expense Tracker!")
    while True:
        print_menu()
        choice = input("Choose an option: ").strip()
        if choice == "9":
            print("Thank you for using Expense Tracker. Goodbye!")
            break
        action = actions.get(choice)
        if action:
            action(expenses)
        else:
            print("Invalid choice. Please select a number from 1 to 9.")


if __name__ == "__main__":
    main()
