import sys
import unittest
from io import StringIO
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from expense_tracker import (  # noqa: E402
    category_totals,
    edit_expense,
    next_id,
    read_amount,
    show_monthly_summary,
    show_total,
)


class ExpenseTrackerTests(unittest.TestCase):
    def setUp(self):
        self.expenses = [
            {"id": 1, "amount": 450.0, "category": "Food", "description": "Lunch", "date": "2026-09-05"},
            {"id": 2, "amount": 120.0, "category": "Travel", "description": "Bus", "date": "2026-09-06"},
            {"id": 5, "amount": 300.0, "category": "Food", "description": "Dinner", "date": "2026-08-20"},
        ]

    def test_next_id_returns_one_after_highest_id(self):
        self.assertEqual(next_id(self.expenses), 6)

    def test_next_id_returns_one_for_empty_list(self):
        self.assertEqual(next_id([]), 1)

    def test_show_total_prints_sum(self):
        with patch("sys.stdout", new_callable=StringIO) as output:
            show_total(self.expenses)
        self.assertIn("Total spending: ₹870.00", output.getvalue())

    def test_category_totals_groups_amounts(self):
        self.assertEqual(category_totals(self.expenses), {"Food": 750.0, "Travel": 120.0})

    def test_invalid_amount_retries_until_valid(self):
        with patch("builtins.input", side_effect=["not-a-number", "-5", "450"]):
            with patch("builtins.print") as printer:
                self.assertEqual(read_amount(), 450.0)
        self.assertEqual(printer.call_count, 2)

    def test_monthly_summary_filters_by_month(self):
        with patch("sys.stdout", new_callable=StringIO) as output:
            show_monthly_summary(self.expenses, "2026-09")
        text = output.getvalue()
        self.assertIn("September 2026", text)
        self.assertIn("Total spent: ₹570.00", text)
        self.assertIn("Food", text)
        self.assertNotIn("₹300.00", text)

    def test_edit_expense_updates_nested_record_and_saves(self):
        with patch("builtins.input", side_effect=["1", "650", "Restaurant", "Dinner"]):
            with patch("expense_tracker.save_expenses") as save:
                edit_expense(self.expenses)
        self.assertEqual(self.expenses[0]["amount"], 650.0)
        self.assertEqual(self.expenses[0]["category"], "Restaurant")
        self.assertEqual(self.expenses[0]["description"], "Dinner")
        save.assert_called_once_with(self.expenses)


if __name__ == "__main__":
    unittest.main()
