import unittest
from models import User, Admin, Transaction
from datetime import datetime

class TestModels(unittest.TestCase):
    def test_admin_password_validation(self):
        admin = Admin(username="testadmin")
        # Test valid password
        self.assertTrue(Admin.validate_password("password123"))
        # Test invalid password (too short)
        self.assertFalse(Admin.validate_password("pass"))
        # Test invalid password (no numbers)
        self.assertFalse(Admin.validate_password("password"))

    def test_admin_username_validation(self):
        # Test valid username
        self.assertTrue(Admin.validate_username("validuser"))
        # Test invalid username (too short)
        self.assertFalse(Admin.validate_username("ab"))
        # Test invalid username (too long)
        self.assertFalse(Admin.validate_username("a" * 81))

    def test_transaction_points_calculation(self):
        transaction = Transaction(
            user_id="test_user",
            count=5,
            amount=1500.0,
            weekly_streak=2,
            transaction_frequency=3
        )
        points = transaction.calculate_points()
        # 5 transactions * 10 points = 50
        # 1500/100 = 15 points
        # 1500/1000 * 50 = 50 points (large transaction bonus)
        # 3 frequency * 5 = 15 points
        # 2 weeks streak * 25 = 50 points
        expected_points = 50 + 15 + 50 + 15 + 50
        self.assertEqual(points, expected_points)
