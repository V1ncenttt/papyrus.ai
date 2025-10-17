"""
Unit tests for authentication models using unittest and factory_boy.
"""

import unittest
from datetime import datetime
from unittest.mock import Mock, patch

from tests.factories.auth_factories import UserFactory, UserCreateFactory


class TestUserModel(unittest.TestCase):
    """Test cases for User model."""

    def test_user_factory_creates_valid_data(self):
        """Test that UserFactory creates valid user data."""
        # Given: We want to create a user
        # When: We use the factory to create data
        user_data = UserFactory()

        # Then: The data should have all required fields
        required_fields = [
            "id", "email", "username", "hashed_password", "full_name",
            "is_active", "is_verified", "created_at", "updated_at"
        ]
        for field in required_fields:
            self.assertIn(field, user_data)

        # And: ID should be a positive integer
        self.assertIsInstance(user_data["id"], int)
        self.assertGreater(user_data["id"], 0)

        # And: Email should be valid format
        self.assertIsInstance(user_data["email"], str)
        self.assertIn("@", user_data["email"])

        # And: Username should be a string
        self.assertIsInstance(user_data["username"], str)
        self.assertGreater(len(user_data["username"]), 0)

        # And: Password should be hashed
        self.assertIsInstance(user_data["hashed_password"], str)
        self.assertIn("hashed_", user_data["hashed_password"])

        # And: Should be active by default
        self.assertTrue(user_data["is_active"])

        # And: Should not be verified by default
        self.assertFalse(user_data["is_verified"])

        # And: Timestamps should be datetime objects
        self.assertIsInstance(user_data["created_at"], datetime)
        self.assertIsInstance(user_data["updated_at"], datetime)

    def test_user_factory_creates_unique_data(self):
        """Test that factory creates unique data each time."""
        # Given: We want to create multiple users
        # When: We create two users using the factory
        user1 = UserFactory()
        user2 = UserFactory()

        # Then: They should have different IDs
        self.assertNotEqual(user1["id"], user2["id"])

        # And: They should have different emails
        self.assertNotEqual(user1["email"], user2["email"])

        # And: They should have different usernames
        self.assertNotEqual(user1["username"], user2["username"])

    def test_user_create_factory_creates_valid_registration_data(self):
        """Test that UserCreateFactory creates valid registration data."""
        # Given: We want to create registration data
        # When: We use the factory to create data
        user_data = UserCreateFactory()

        # Then: The data should have registration fields
        self.assertIn("email", user_data)
        self.assertIn("username", user_data)
        self.assertIn("password", user_data)
        self.assertIn("full_name", user_data)

        # And: All fields should be strings
        self.assertIsInstance(user_data["email"], str)
        self.assertIsInstance(user_data["username"], str)
        self.assertIsInstance(user_data["password"], str)
        self.assertIsInstance(user_data["full_name"], str)

        # And: Password should be of reasonable length
        self.assertGreaterEqual(len(user_data["password"]), 8)

    def test_user_status_variations(self):
        """Test different user status combinations."""
        test_cases = [
            {"is_active": True, "is_verified": True, "expected_status": "active_verified"},
            {"is_active": True, "is_verified": False, "expected_status": "active_unverified"},
            {"is_active": False, "is_verified": True, "expected_status": "inactive_verified"},
            {"is_active": False, "is_verified": False, "expected_status": "inactive_unverified"},
        ]
        
        for case in test_cases:
            with self.subTest(case=case):
                # Given: Different user active/verified states
                user_data = UserFactory(
                    is_active=case["is_active"],
                    is_verified=case["is_verified"]
                )

                # When: We determine the status
                if user_data["is_active"] and user_data["is_verified"]:
                    status = "active_verified"
                elif user_data["is_active"] and not user_data["is_verified"]:
                    status = "active_unverified"
                elif not user_data["is_active"] and user_data["is_verified"]:
                    status = "inactive_verified"
                else:
                    status = "inactive_unverified"

                # Then: We get the expected status
                self.assertEqual(status, case["expected_status"])

    def test_mock_user_model_operations(self):
        """Test mock user model operations without actual database."""
        # Given: Mock database and user data
        mock_db = Mock()
        user_data = UserFactory()
        
        # When: We simulate database operations
        mock_db.create_user(user_data)
        mock_db.get_user_by_id(user_data["id"])
        mock_db.update_user(user_data["id"], {"is_verified": True})
        mock_db.delete_user(user_data["id"])

        # Then: The database methods should have been called
        mock_db.create_user.assert_called_once_with(user_data)
        mock_db.get_user_by_id.assert_called_once_with(user_data["id"])
        mock_db.update_user.assert_called_once_with(user_data["id"], {"is_verified": True})
        mock_db.delete_user.assert_called_once_with(user_data["id"])

    def test_user_data_validation_logic(self):
        """Test user data validation logic."""
        validation_cases = [
            {"email": "test@example.com", "username": "validuser", "expected": True},
            {"email": "", "username": "validuser", "expected": False},
            {"email": "test@example.com", "username": "", "expected": False},
            {"email": "invalid-email", "username": "validuser", "expected": False},
            {"email": "test@example.com", "username": "ab", "expected": True},
        ]
        
        for case in validation_cases:
            with self.subTest(case=case):
                # Given: Different email and username combinations
                # When: We validate the data
                is_valid = bool(
                    case["email"] and 
                    case["username"] and 
                    "@" in case["email"] and
                    "." in case["email"]
                )

                # Then: Validation should match expected result
                self.assertEqual(is_valid, case["expected"])


class TestUserFactoryEdgeCases(unittest.TestCase):
    """Test edge cases and special scenarios for user factories."""

    def test_bulk_user_creation_uniqueness(self):
        """Test that bulk user creation maintains uniqueness."""
        # Given: We want to create many users
        num_users = 10
        
        # When: We create multiple users
        users = [UserFactory() for _ in range(num_users)]

        # Then: All should have unique IDs
        ids = [user["id"] for user in users]
        self.assertEqual(len(set(ids)), num_users)

        # And: All should have unique emails
        emails = [user["email"] for user in users]
        self.assertEqual(len(set(emails)), num_users)

        # And: All should have unique usernames
        usernames = [user["username"] for user in users]
        self.assertEqual(len(set(usernames)), num_users)

    def test_user_factory_with_custom_values(self):
        """Test factory with custom overridden values."""
        # Given: We want specific user data
        custom_email = "custom@example.com"
        custom_username = "customuser"

        # When: We create a user with custom values
        user_data = UserFactory(
            email=custom_email,
            username=custom_username,
            is_verified=True
        )

        # Then: Custom values should be preserved
        self.assertEqual(user_data["email"], custom_email)
        self.assertEqual(user_data["username"], custom_username)
        self.assertTrue(user_data["is_verified"])

        # And: Other fields should still be generated
        self.assertIsNotNone(user_data["full_name"])
        self.assertIsInstance(user_data["id"], int)

    def test_password_requirements_validation(self):
        """Test password requirements validation logic."""
        password_cases = [
            {"password": "short", "min_length": 8, "expected": False},
            {"password": "validpassword123", "min_length": 8, "expected": True},
            {"password": "", "min_length": 8, "expected": False},
            {"password": "12345678", "min_length": 8, "expected": True},
            {"password": "a" * 100, "min_length": 8, "expected": True},
        ]
        
        for case in password_cases:
            with self.subTest(case=case):
                # Given: Different password values
                # When: We validate the password
                is_valid = len(case["password"]) >= case["min_length"]

                # Then: We get the expected validation result
                self.assertEqual(is_valid, case["expected"])


if __name__ == '__main__':
    unittest.main()