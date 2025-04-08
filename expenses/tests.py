from django.test import TestCase
import polars as pl
from .views import clean_data


class CleanDataTests(TestCase):
    def test_clean_data_not_clean1(self):
        data = [
            ("Twitch", 5.89, "Entertainment", "2024-03-01"),
            ("Publix", 125.78, "Groceries", "2024-03-15"),
            ("Amazon", 67.52, "Other", "2024-03-16"),
            ("Twitch", 5.89, "Entertainment", "2024-04-01"),
            ("Rent", 1200.00, "Housing", "2024-03-12"),
            ("Electric Bill", 90.00, "Utilities", "2024-03-11"),
            ("Rent", 1200.00, "Housing", "2024-04-12"),
            ("Electric Bill", 90.00, "Utilities", "2024-04-11"),
            ("Publix", 142.33, "Groceries", "2024-03-29")
        ]
        df = pl.DataFrame(data, schema=["Name", "Amount", "Category", "Date"])

        answer = pl.DataFrame({
            "Label": [
                "Twitch",
                "Publix",
                "Amazon",
                "Rent",
                "Electric Bill",
                "Publix"
            ],
            "Amount": [
                5.89,
                125.78,
                67.52,
                1200.00,
                90.00,
                142.33
            ],
            "Category": [
                "Entertainment",
                "Groceries",
                "Other",
                "Housing",
                "Utilities",
                "Groceries"
            ],
            "startDate": [
                "2024-03-01",
                "2024-03-15",
                "2024-03-16",
                "2024-03-12",
                "2024-03-11",
                "2024-03-29"
            ],
            "frequency": [
                "Monthly",
                None,
                None,
                "Monthly",
                "Monthly",
                None
            ],
            "principal": [
                None,
                None,
                None,
                None,
                None,
                None
            ],
            "interestRate": [
                None,
                None,
                None,
                None,
                None,
                None
            ],
            "termLength": [
                None,
                None,
                None,
                None,
                None,
                None
            ]
        }).sort("startDate").to_dicts()

        result = clean_data(df)
        self.assertEqual(result, answer)

    def test_clean_data_not_clean2(self):
        data = [
            # Entertainment
            ("Twitch", 5.89, "Entertainment", "2024-03-01"),
            ("Twitch", 5.89, "Entertainment", "2024-04-01"),
            ("Twitch", 5.89, "Entertainment", "2024-05-01"),
            ("Netflix", 15.49, "Entertainment", "2024-03-02"),
            ("Netflix", 15.49, "Entertainment", "2024-04-03"),
            ("Netflix", 15.49, "Entertainment", "2024-05-02"),

            # Groceries
            ("Publix", 125.78, "Groceries", "2024-03-15"),
            ("Publix", 142.33, "Groceries", "2024-03-29"),
            ("Publix", 98.21, "Groceries", "2024-04-14"),
            ("Publix", 110.87, "Groceries", "2024-05-01"),
            ("Walmart", 210.45, "Groceries", "2024-03-18"),
            ("Walmart", 199.99, "Groceries", "2024-04-18"),

            # Housing
            ("Rent", 1200.00, "Housing", "2024-03-12"),
            ("Rent", 1200.00, "Housing", "2024-04-12"),
            ("Rent", 1200.00, "Housing", "2024-05-12"),

            # Utilities
            ("Electric Bill", 90.00, "Utilities", "2024-03-11"),
            ("Electric Bill", 90.00, "Utilities", "2024-04-11"),
            ("Electric Bill", 92.00, "Utilities", "2024-05-11"),  # Slight variance
            ("Water Bill", 45.00, "Utilities", "2024-03-13"),
            ("Water Bill", 45.00, "Utilities", "2024-04-13"),
            ("Water Bill", 45.00, "Utilities", "2024-05-13"),

            # Other
            ("Amazon", 67.52, "Other", "2024-03-16"),
            ("Amazon", 120.00, "Other", "2024-04-03"),
            ("Amazon", 55.32, "Other", "2024-05-02"),
            ("Etsy", 24.99, "Other", "2024-03-20"),
            ("Etsy", 18.75, "Other", "2024-04-22"),
            ("Leetcode Premium", 10.00, "Other", "2023-03-11"),
            ("Leetcode Premium", 10.00, "Other", "2024-03-11"),

            # == Edge Cases ==

            # Future recurrence
            ("Twitch", 5.89, "Entertainment", "2025-03-01"),

            # Earlier than base window
            ("Netflix", 15.49, "Entertainment", "2023-12-02"),

            # Past entry for Rent
            ("Rent", 1200.00, "Housing", "2023-12-12"),
        ]

        df = pl.DataFrame(
            data, schema=["Name", "Amount", "Category", "Date"], orient="row")

        answer_data = [
            ("Twitch", 5.89, "Entertainment",
             "2024-03-01", "Monthly", None, None, None),
            ("Netflix", 15.49, "Entertainment",
             "2023-12-02", "Monthly", None, None, None),
            ("Publix", 125.78, "Groceries", "2024-03-15", None, None, None, None),
            ("Publix", 142.33, "Groceries", "2024-03-29", None, None, None, None),
            ("Publix", 98.21, "Groceries", "2024-04-14", None, None, None, None),
            ("Publix", 110.87, "Groceries", "2024-05-01", None, None, None, None),
            ("Walmart", 210.45, "Groceries", "2024-03-18", None, None, None, None),
            ("Walmart", 199.99, "Groceries", "2024-04-18", None, None, None, None),
            ("Rent", 1200.00, "Housing", "2023-12-12", "Monthly", None, None, None),
            ("Electric Bill", 90.00, "Utilities",
             "2024-03-11", "Monthly", None, None, None),
            ("Electric Bill", 92.00, "Utilities",
             "2024-05-11", None, None, None, None),
            ("Water Bill", 45.00, "Utilities",
             "2024-03-13", "Monthly", None, None, None),
            ("Amazon", 67.52, "Other", "2024-03-16", None, None, None, None),
            ("Amazon", 120.00, "Other", "2024-04-03", None, None, None, None),
            ("Amazon", 55.32, "Other", "2024-05-02", None, None, None, None),
            ("Etsy", 24.99, "Other", "2024-03-20", None, None, None, None),
            ("Etsy", 18.75, "Other", "2024-04-22", None, None, None, None),
            ("Leetcode Premium", 10.00, "Other",
             "2023-03-11", "Annually", None, None, None),
        ]

        answer = pl.DataFrame(answer_data, schema=[
            "Label", "Amount", "Category", "startDate",
            "frequency", "principal", "interestRate", "termLength"
        ], orient="row").sort("startDate").to_dicts()


        result = clean_data(df)


        self.assertEqual(result, answer)
