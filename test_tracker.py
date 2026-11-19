"""
Unit Tests for Personal Expense and Budget Tracker
Tests core calculations, data persistence, and budget alert logic.
"""

import os
import unittest
import tempfile
import json
from expense_tracker import (
    load_data,
    save_data,
    generate_next_id,
    calculate_totals,
    calculate_balance,
    get_monthly_expense_total
)


class TestExpenseTracker(unittest.TestCase):

    def setUp(self):
        # Create a temporary file for test data
        self.temp_file = tempfile.NamedTemporaryFile(delete=False)
        self.temp_file.close()
        self.test_path = self.temp_file.name

        self.sample_data = {
            "transactions": [
                {
                    "id": 1,
                    "type": "income",
                    "amount": 3000.0,
                    "category": "Salary",
                    "date": "2026-11-01",
                    "description": "November Salary"
                },
                {
                    "id": 2,
                    "type": "expense",
                    "amount": 400.0,
                    "category": "Groceries",
                    "date": "2026-11-03",
                    "description": "Weekly grocery"
                },
                {
                    "id": 3,
                    "type": "expense",
                    "amount": 200.0,
                    "category": "Utilities",
                    "date": "2026-11-10",
                    "description": "Electricity & Water"
                },
                {
                    "id": 4,
                    "type": "income",
                    "amount": 500.0,
                    "category": "Freelance",
                    "date": "2026-10-15",
                    "description": "Consulting gig"
                },
                {
                    "id": 5,
                    "type": "expense",
                    "amount": 150.0,
                    "category": "Entertainment",
                    "date": "2026-10-20",
                    "description": "Concert ticket"
                }
            ],
            "monthly_budgets": {
                "2026-11": 800.0,
                "2026-10": 100.0
            }
        }

    def tearDown(self):
        if os.path.exists(self.test_path):
            os.remove(self.test_path)

    def test_save_and_load_data(self):
        """Verify saving data to file and loading it back maintains integrity."""
        save_result = save_data(self.sample_data, self.test_path)
        self.assertTrue(save_result)

        loaded_data = load_data(self.test_path)
        self.assertEqual(len(loaded_data["transactions"]), 5)
        self.assertEqual(loaded_data["monthly_budgets"]["2026-11"], 800.0)

    def test_load_nonexistent_file(self):
        """Loading a non-existent file returns a clean default data structure."""
        non_existent = "non_existent_file_xyz_123.json"
        data = load_data(non_existent)
        self.assertEqual(data, {"transactions": [], "monthly_budgets": {}})

    def test_load_corrupted_file(self):
        """Loading a corrupted or empty file safely falls back to defaults without crashing."""
        with open(self.test_path, "w") as f:
            f.write("INVALID JSON CONTENT {{{")
        data = load_data(self.test_path)
        self.assertEqual(data, {"transactions": [], "monthly_budgets": {}})

    def test_generate_next_id(self):
        """Test ID generation handles empty and populated lists."""
        self.assertEqual(generate_next_id([]), 1)
        self.assertEqual(generate_next_id(self.sample_data["transactions"]), 6)

    def test_calculate_totals(self):
        """Test calculation of total income and total expenses."""
        income, expenses = calculate_totals(self.sample_data)
        # Income: 3000 + 500 = 3500
        # Expenses: 400 + 200 + 150 = 750
        self.assertEqual(income, 3500.0)
        self.assertEqual(expenses, 750.0)

    def test_calculate_balance(self):
        """Test calculation of available balance."""
        balance = calculate_balance(self.sample_data)
        # Balance = 3500 - 750 = 2750
        self.assertEqual(balance, 2750.0)

    def test_get_monthly_expense_total(self):
        """Test filtering and summing expenses for specific months."""
        nov_expense = get_monthly_expense_total(self.sample_data, "2026-11")
        self.assertEqual(nov_expense, 600.0)  # 400 + 200

        oct_expense = get_monthly_expense_total(self.sample_data, "2026-10")
        self.assertEqual(oct_expense, 150.0)  # 150

        empty_month = get_monthly_expense_total(self.sample_data, "2026-09")
        self.assertEqual(empty_month, 0.0)


if __name__ == "__main__":
    unittest.main()
