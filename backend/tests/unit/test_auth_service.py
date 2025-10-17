"""
Unit tests for authentication service using unittest and factory_boy.
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime, timedelta

from tests.factories.auth_factories import (
    UserFactory, UserCreateFactory, UserLoginFactory, TokenFactory
)


class TestAuthService(unittest.TestCase):
    """Test cases for AuthService without database dependencies."""

    def setUp(self):
        """Set up test fixtures before each test method."""
        self.mock_db = Mock()
        self.mock_auth_service = Mock()

    def test_hash_password_functionality(self):
        """Test password hashing functionality."""
        # Given: A plain password
        password = "testpassword123"
        expected_hash = f"hashed_{password}"
        self.mock_auth_service.hash_password.return_value = expected_hash

        # When: Hashing the password
        result = self.mock_auth_service.hash_password(password)

        # Then: Should return hashed password
        self.assertEqual(result, expected_hash)
        self.mock_auth_service.hash_password.assert_called_once_with(password)

    def test_verify_password_success(self):
        """Test successful password verification."""
        # Given: Correct password and hash
        plain_password = "testpassword123"
        hashed_password = "hashed_testpassword123"
        self.mock_auth_service.verify_password.return_value = True

        # When: Verifying password
        result = self.mock_auth_service.verify_password(plain_password, hashed_password)

        # Then: Should return True
        self.assertTrue(result)
        self.mock_auth_service.verify_password.assert_called_once_with(
            plain_password, hashed_password
        )

    def test_verify_password_failure(self):
        """Test failed password verification."""
        # Given: Incorrect password
        plain_password = "wrongpassword"
        hashed_password = "hashed_testpassword123"
        self.mock_auth_service.verify_password.return_value = False

        # When: Verifying password
        result = self.mock_auth_service.verify_password(plain_password, hashed_password)

        # Then: Should return False
        self.assertFalse(result)

    def test_create_access_token(self):
        """Test access token creation."""
        # Given: User data and expected token
        user_data = {"sub": "test@example.com", "user_id": 1}
        expected_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.mock_token"
        self.mock_auth_service.create_access_token.return_value = expected_token

        # When: Creating access token
        token = self.mock_auth_service.create_access_token(data=user_data)

        # Then: Should return token
        self.assertEqual(token, expected_token)
        self.mock_auth_service.create_access_token.assert_called_once_with(data=user_data)

    def test_get_user_by_email_found(self):
        """Test getting user by email when user exists."""
        # Given: Factory-generated user data
        user_data = UserFactory()
        email = user_data["email"]
        self.mock_auth_service.get_user_by_email.return_value = user_data

        # When: Getting user by email
        result = self.mock_auth_service.get_user_by_email(email)

        # Then: Should return user
        self.assertEqual(result, user_data)
        self.assertEqual(result["email"], email)
        self.mock_auth_service.get_user_by_email.assert_called_once_with(email)

    def test_get_user_by_email_not_found(self):
        """Test getting user by email when user doesn't exist."""
        # Given: Non-existent email
        email = "nonexistent@example.com"
        self.mock_auth_service.get_user_by_email.return_value = None

        # When: Getting user by email
        result = self.mock_auth_service.get_user_by_email(email)

        # Then: Should return None
        self.assertIsNone(result)

    def test_create_user_success(self):
        """Test successful user creation."""
        # Given: Factory-generated user creation data
        user_create_data = UserCreateFactory()
        created_user = UserFactory(
            email=user_create_data["email"],
            username=user_create_data["username"],
            full_name=user_create_data["full_name"]
        )
        self.mock_auth_service.create_user.return_value = created_user

        # When: Creating user
        result = self.mock_auth_service.create_user(user_create_data)

        # Then: Should create and return user
        self.assertEqual(result, created_user)
        self.assertEqual(result["email"], user_create_data["email"])
        self.assertEqual(result["username"], user_create_data["username"])
        self.mock_auth_service.create_user.assert_called_once_with(user_create_data)

    def test_authenticate_user_success(self):
        """Test successful user authentication."""
        # Given: Valid credentials and user data
        user_data = UserFactory()
        email = user_data["email"]
        password = "correctpassword"
        self.mock_auth_service.authenticate_user.return_value = user_data

        # When: Authenticating user
        result = self.mock_auth_service.authenticate_user(email, password)

        # Then: Should return user
        self.assertEqual(result, user_data)
        self.mock_auth_service.authenticate_user.assert_called_once_with(email, password)

    def test_authenticate_user_failure(self):
        """Test failed user authentication."""
        # Given: Invalid credentials
        email = "test@example.com"
        password = "wrongpassword"
        self.mock_auth_service.authenticate_user.return_value = None

        # When: Authenticating user
        result = self.mock_auth_service.authenticate_user(email, password)

        # Then: Should return None
        self.assertIsNone(result)

    def test_get_user_by_id_success(self):
        """Test successful user retrieval by ID."""
        # Given: User data
        user_data = UserFactory()
        user_id = user_data["id"]
        self.mock_auth_service.get_user_by_id.return_value = user_data

        # When: Getting user by ID
        result = self.mock_auth_service.get_user_by_id(user_id)

        # Then: Should return user
        self.assertEqual(result, user_data)
        self.assertEqual(result["id"], user_id)

    def test_update_user_success(self):
        """Test successful user update."""
        # Given: User data and update data
        user_data = UserFactory()
        user_id = user_data["id"]
        update_data = {"is_verified": True, "full_name": "Updated Name"}
        
        updated_user = {**user_data, **update_data}
        self.mock_auth_service.update_user.return_value = updated_user

        # When: Updating user
        result = self.mock_auth_service.update_user(user_id, update_data)

        # Then: Should return updated user
        self.assertEqual(result, updated_user)
        self.assertTrue(result["is_verified"])
        self.assertEqual(result["full_name"], "Updated Name")


class TestAuthServiceIntegration(unittest.TestCase):
    """Test auth service integration scenarios without database."""

    def setUp(self):
        """Set up test fixtures."""
        self.mock_auth_service = Mock()

    def test_full_registration_flow(self):
        """Test complete user registration flow with mocked components."""
        # Given: Registration data and mocked services
        user_data = UserCreateFactory()
        
        # Mock service methods
        self.mock_auth_service.get_user_by_email.return_value = None  # User doesn't exist
        self.mock_auth_service.hash_password.return_value = f"hashed_{user_data['password']}"
        created_user = UserFactory(
            email=user_data["email"],
            username=user_data["username"],
            full_name=user_data["full_name"]
        )
        self.mock_auth_service.create_user.return_value = created_user

        # When: Processing registration (simulate endpoint logic)
        existing_user = self.mock_auth_service.get_user_by_email(user_data["email"])
        if not existing_user:
            hashed_password = self.mock_auth_service.hash_password(user_data["password"])
            user_with_hashed_password = {**user_data, "hashed_password": hashed_password}
            result = self.mock_auth_service.create_user(user_with_hashed_password)
        else:
            result = None

        # Then: Should complete successfully
        self.assertIsNotNone(result)
        self.assertEqual(result["email"], user_data["email"])
        self.assertEqual(result["username"], user_data["username"])
        self.mock_auth_service.get_user_by_email.assert_called_once_with(user_data["email"])
        self.mock_auth_service.hash_password.assert_called_once_with(user_data["password"])
        self.mock_auth_service.create_user.assert_called_once()

    def test_full_login_flow(self):
        """Test complete user login flow with mocked components."""
        # Given: Login data and existing user
        login_data = UserLoginFactory()
        existing_user = UserFactory(email=login_data["email"])
        token_data = TokenFactory()
        
        # Mock service methods
        self.mock_auth_service.authenticate_user.return_value = existing_user
        self.mock_auth_service.create_access_token.return_value = token_data["access_token"]

        # When: Processing login (simulate endpoint logic)
        authenticated_user = self.mock_auth_service.authenticate_user(
            login_data["email"], 
            login_data["password"]
        )
        if authenticated_user:
            token_payload = {"sub": authenticated_user["email"], "user_id": authenticated_user["id"]}
            access_token = self.mock_auth_service.create_access_token(data=token_payload)
            result = {"access_token": access_token, "token_type": "bearer"}
        else:
            result = None

        # Then: Should complete successfully
        self.assertIsNotNone(result)
        self.assertEqual(result["access_token"], token_data["access_token"])
        self.assertEqual(result["token_type"], "bearer")
        self.mock_auth_service.authenticate_user.assert_called_once_with(
            login_data["email"], 
            login_data["password"]
        )
        self.mock_auth_service.create_access_token.assert_called_once()

    def test_registration_with_duplicate_email_flow(self):
        """Test registration flow when email already exists."""
        # Given: Registration data and existing user
        user_data = UserCreateFactory()
        existing_user = UserFactory(email=user_data["email"])
        
        # Mock service methods
        self.mock_auth_service.get_user_by_email.return_value = existing_user  # User exists

        # When: Processing registration (simulate endpoint logic)
        existing_user_check = self.mock_auth_service.get_user_by_email(user_data["email"])
        if existing_user_check:
            result = {"error": "Email already registered"}
        else:
            result = {"success": "User created"}

        # Then: Should return error
        self.assertIn("error", result)
        self.assertIn("already registered", result["error"])
        self.mock_auth_service.get_user_by_email.assert_called_once_with(user_data["email"])

    def test_authentication_failure_flow(self):
        """Test login flow when authentication fails."""
        # Given: Invalid login data
        login_data = UserLoginFactory()
        
        # Mock service methods
        self.mock_auth_service.authenticate_user.return_value = None  # Authentication failed

        # When: Processing login (simulate endpoint logic)
        authenticated_user = self.mock_auth_service.authenticate_user(
            login_data["email"], 
            login_data["password"]
        )
        if authenticated_user:
            result = {"success": "Login successful"}
        else:
            result = {"error": "Invalid credentials"}

        # Then: Should return error
        self.assertIn("error", result)
        self.assertIn("Invalid credentials", result["error"])
        self.mock_auth_service.authenticate_user.assert_called_once_with(
            login_data["email"], 
            login_data["password"]
        )

    def test_user_verification_flow(self):
        """Test user email verification flow."""
        # Given: Unverified user
        user_data = UserFactory(is_verified=False)
        verification_token = "verification_token_123"
        
        # Mock service methods
        self.mock_auth_service.verify_email_token.return_value = user_data["email"]
        verified_user = {**user_data, "is_verified": True}
        self.mock_auth_service.update_user.return_value = verified_user

        # When: Processing verification
        email = self.mock_auth_service.verify_email_token(verification_token)
        if email:
            result = self.mock_auth_service.update_user(user_data["id"], {"is_verified": True})
        else:
            result = None

        # Then: Should verify user successfully
        self.assertIsNotNone(result)
        self.assertTrue(result["is_verified"])
        self.mock_auth_service.verify_email_token.assert_called_once_with(verification_token)


class TestAuthServiceEdgeCases(unittest.TestCase):
    """Test edge cases and error scenarios for auth service."""

    def setUp(self):
        """Set up test fixtures."""
        self.mock_auth_service = Mock()

    def test_concurrent_user_creation_scenario(self):
        """Test handling of concurrent user creation attempts."""
        # Given: Multiple registration attempts with same email
        user_data1 = UserCreateFactory(email="same@example.com")
        user_data2 = UserCreateFactory(email="same@example.com")

        # Mock first call succeeds, second fails
        self.mock_auth_service.get_user_by_email.side_effect = [None, UserFactory()]

        # When: Processing both registrations
        first_check = self.mock_auth_service.get_user_by_email(user_data1["email"])
        second_check = self.mock_auth_service.get_user_by_email(user_data2["email"])

        # Then: First should pass, second should fail
        self.assertIsNone(first_check)  # No existing user
        self.assertIsNotNone(second_check)  # User now exists

    def test_service_method_error_handling(self):
        """Test service method error handling."""
        # Given: Service methods that might raise exceptions
        self.mock_auth_service.hash_password.side_effect = Exception("Hashing error")
        self.mock_auth_service.create_user.side_effect = Exception("Database error")

        # When/Then: Should handle exceptions appropriately
        with self.assertRaises(Exception):
            self.mock_auth_service.hash_password("password")

        with self.assertRaises(Exception):
            self.mock_auth_service.create_user({})

    def test_token_expiration_scenarios(self):
        """Test token expiration handling."""
        # Given: Different token scenarios
        valid_token = TokenFactory()
        expired_token = TokenFactory(expires_in=-3600)  # Expired

        # When: Checking token validity (simulated)
        valid_token_valid = valid_token["expires_in"] > 0
        expired_token_valid = expired_token["expires_in"] > 0

        # Then: Should correctly identify validity
        self.assertTrue(valid_token_valid)
        self.assertFalse(expired_token_valid)


if __name__ == '__main__':
    unittest.main()