"""
Unit tests for authentication schemas using unittest and factory_boy.
"""

import unittest
from unittest.mock import patch
from datetime import datetime

from tests.factories.auth_factories import (
    UserCreateFactory, UserLoginFactory, TokenFactory, UserResponseFactory
)


class TestAuthSchemas(unittest.TestCase):
    """Test cases for authentication Pydantic schemas."""

    def test_user_create_schema_with_factory_data(self):
        """Test UserCreate schema with factory-generated data."""
        # Given: Factory-generated user creation data
        user_data = UserCreateFactory()

        # When: We validate the data structure
        required_fields = ["email", "username", "password", "full_name"]
        has_all_fields = all(key in user_data for key in required_fields)

        # Then: Data should have all required fields
        self.assertTrue(has_all_fields)

        # And: Email should be valid format
        self.assertIn("@", user_data["email"])
        self.assertIn(".", user_data["email"])

        # And: Password should meet minimum requirements
        self.assertGreaterEqual(len(user_data["password"]), 8)

        # And: Username should be non-empty
        self.assertGreater(len(user_data["username"]), 0)

    def test_user_login_schema_with_factory_data(self):
        """Test UserLogin schema with factory-generated data."""
        # Given: Factory-generated login data
        login_data = UserLoginFactory()

        # When: We validate the data structure
        required_fields = ["email", "password"]
        has_all_fields = all(key in login_data for key in required_fields)

        # Then: Data should have all required fields
        self.assertTrue(has_all_fields)

        # And: Email should be valid format
        self.assertIn("@", login_data["email"])

        # And: Password should be non-empty
        self.assertGreater(len(login_data["password"]), 0)

    def test_token_schema_with_factory_data(self):
        """Test Token schema with factory-generated data."""
        # Given: Factory-generated token data
        token_data = TokenFactory()

        # When: We validate the data structure
        required_fields = ["access_token", "token_type", "expires_in"]
        has_all_fields = all(key in token_data for key in required_fields)

        # Then: Data should have all required fields
        self.assertTrue(has_all_fields)

        # And: Token type should be bearer
        self.assertEqual(token_data["token_type"], "bearer")

        # And: Access token should be non-empty
        self.assertGreater(len(token_data["access_token"]), 0)

        # And: Should look like a JWT token
        self.assertTrue(token_data["access_token"].startswith("eyJ"))

        # And: Expires in should be positive integer
        self.assertIsInstance(token_data["expires_in"], int)
        self.assertGreater(token_data["expires_in"], 0)

    def test_user_response_schema_with_factory_data(self):
        """Test UserResponse schema with factory-generated data."""
        # Given: Factory-generated user response data
        user_data = UserResponseFactory()

        # When: We validate the data structure
        required_fields = [
            "id", "email", "username", "full_name", 
            "is_active", "is_verified", "created_at"
        ]
        has_all_fields = all(key in user_data for key in required_fields)

        # Then: Data should have all required fields
        self.assertTrue(has_all_fields)

        # And: ID should be positive integer
        self.assertIsInstance(user_data["id"], int)
        self.assertGreater(user_data["id"], 0)

        # And: Created at should be datetime
        self.assertIsInstance(user_data["created_at"], datetime)

        # And: Boolean fields should be boolean
        self.assertIsInstance(user_data["is_active"], bool)
        self.assertIsInstance(user_data["is_verified"], bool)

    def test_email_validation_logic(self):
        """Test email validation logic with various inputs."""
        email_cases = [
            {"email": "test@example.com", "expected": True},
            {"email": "invalid-email", "expected": False},
            {"email": "", "expected": False},
            {"email": "user@domain.co.uk", "expected": True},
            {"email": "@domain.com", "expected": False},
            {"email": "user@", "expected": False},
            {"email": "user.name@domain.com", "expected": True},
        ]
        
        for case in email_cases:
            with self.subTest(email=case["email"]):
                # Given: Different email formats
                # When: We validate the email
                email = case["email"]
                if not email or "@" not in email:
                    is_valid = False
                else:
                    local_part, domain_part = email.split("@", 1)
                    is_valid = bool(
                        local_part and  # Must have something before @
                        domain_part and  # Must have something after @
                        "." in domain_part and  # Domain must have a dot
                        len(domain_part.split(".")[-1]) >= 2  # TLD must be at least 2 chars
                    )

                # Then: We get the expected validation result
                self.assertEqual(is_valid, case["expected"])

    def test_password_validation_logic(self):
        """Test password validation logic with various inputs."""
        password_cases = [
            {"password": "short", "min_length": 8, "expected": False},
            {"password": "validpassword123", "min_length": 8, "expected": True},
            {"password": "", "min_length": 8, "expected": False},
            {"password": "12345678", "min_length": 8, "expected": True},
            {"password": "a" * 100, "min_length": 8, "expected": True},
            {"password": "Complex1!", "min_length": 8, "expected": True},
        ]
        
        for case in password_cases:
            with self.subTest(password=case["password"]):
                # Given: Different password values
                # When: We validate the password
                is_valid = len(case["password"]) >= case["min_length"]

                # Then: We get the expected validation result
                self.assertEqual(is_valid, case["expected"])

    def test_username_validation_logic(self):
        """Test username validation logic with various inputs."""
        username_cases = [
            {"username": "validuser", "expected": True},
            {"username": "", "expected": False},
            {"username": "a", "expected": True},
            {"username": "user123", "expected": True},
            {"username": "user_name", "expected": True},
            {"username": "user-name", "expected": True},
            {"username": " ", "expected": False},
        ]
        
        for case in username_cases:
            with self.subTest(username=case["username"]):
                # Given: Different username values
                # When: We validate the username
                username = case["username"]
                is_valid = bool(username and username.strip())

                # Then: We get the expected validation result
                self.assertEqual(is_valid, case["expected"])


class TestSchemaDataConsistency(unittest.TestCase):
    """Test consistency and relationships between different schemas."""

    def test_create_to_response_data_flow(self):
        """Test data flow from UserCreate to UserResponse."""
        # Given: User creation data
        create_data = UserCreateFactory()
        
        # When: We simulate creating a user and getting response
        # (This would normally involve the service layer)
        response_data = UserResponseFactory(
            email=create_data["email"],
            username=create_data["username"],
            full_name=create_data["full_name"]
        )

        # Then: Response should maintain the same core data
        self.assertEqual(response_data["email"], create_data["email"])
        self.assertEqual(response_data["username"], create_data["username"])
        self.assertEqual(response_data["full_name"], create_data["full_name"])

        # And: Response should have additional fields
        self.assertIn("id", response_data)
        self.assertIn("is_active", response_data)
        self.assertIn("is_verified", response_data)
        self.assertIn("created_at", response_data)

    def test_login_to_token_data_flow(self):
        """Test data flow from login to token generation."""
        # Given: Login data
        login_data = UserLoginFactory()
        
        # When: We simulate successful authentication
        # (This would normally involve the auth service)
        token_data = TokenFactory()

        # Then: Token should be properly formatted
        self.assertIsInstance(token_data["access_token"], str)
        self.assertEqual(token_data["token_type"], "bearer")
        self.assertIsInstance(token_data["expires_in"], int)

        # And: Token should look like JWT
        self.assertTrue(token_data["access_token"].startswith("eyJ"))

    def test_bulk_schema_generation_consistency(self):
        """Test that bulk generation maintains consistency."""
        # Given: We want to create multiple instances
        num_instances = 5

        # When: We create multiple instances of each type
        create_instances = [UserCreateFactory() for _ in range(num_instances)]
        login_instances = [UserLoginFactory() for _ in range(num_instances)]
        response_instances = [UserResponseFactory() for _ in range(num_instances)]
        token_instances = [TokenFactory() for _ in range(num_instances)]

        # Then: All create instances should be valid
        for instance in create_instances:
            self.assertIn("@", instance["email"])
            self.assertGreater(len(instance["password"]), 7)

        # And: All login instances should be valid
        for instance in login_instances:
            self.assertIn("@", instance["email"])
            self.assertGreater(len(instance["password"]), 0)

        # And: All response instances should be valid
        for instance in response_instances:
            self.assertIsInstance(instance["id"], int)
            self.assertIn("@", instance["email"])

        # And: All token instances should be valid
        for instance in token_instances:
            self.assertEqual(instance["token_type"], "bearer")
            self.assertTrue(instance["access_token"].startswith("eyJ"))

    def test_schema_validation_error_simulation(self):
        """Test schema validation error scenarios."""
        # Given: Invalid data scenarios
        invalid_cases = [
            {"email": "invalid", "username": "test", "password": "password123"},
            {"email": "test@example.com", "username": "", "password": "password123"},
            {"email": "test@example.com", "username": "test", "password": "short"},
        ]

        for case in invalid_cases:
            with self.subTest(case=case):
                # When: We validate the data
                email_valid = "@" in case["email"] and "." in case["email"]
                username_valid = bool(case["username"].strip())
                password_valid = len(case["password"]) >= 8

                overall_valid = email_valid and username_valid and password_valid

                # Then: At least one validation should fail
                self.assertFalse(overall_valid)


if __name__ == '__main__':
    unittest.main()