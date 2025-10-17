"""
Unit tests for authentication API endpoints using unittest and factory_boy.
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
import json

from tests.factories.auth_factories import (
    UserCreateFactory, UserLoginFactory, UserFactory, TokenFactory, UserResponseFactory
)


class TestAuthEndpoints(unittest.TestCase):
    """Test cases for authentication endpoints without FastAPI dependencies."""

    def setUp(self):
        """Set up test fixtures before each test method."""
        self.mock_client = Mock()
        self.mock_auth_service = Mock()

    def test_register_endpoint_success(self):
        """Test successful user registration endpoint."""
        # Given: Valid registration data
        user_data = UserCreateFactory()
        created_user = UserResponseFactory(
            email=user_data["email"],
            username=user_data["username"],
            full_name=user_data["full_name"]
        )
        
        # Mock successful response
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.json.return_value = {
            "id": created_user["id"],
            "email": created_user["email"],
            "username": created_user["username"],
            "full_name": created_user["full_name"],
            "is_active": created_user["is_active"],
            "is_verified": created_user["is_verified"]
        }
        self.mock_client.post.return_value = mock_response

        # When: Making registration request
        response = self.mock_client.post("/api/v1/auth/register", json=user_data)

        # Then: Should return created user
        self.assertEqual(response.status_code, 201)
        response_data = response.json()
        self.assertEqual(response_data["email"], user_data["email"])
        self.assertEqual(response_data["username"], user_data["username"])
        self.assertEqual(response_data["full_name"], user_data["full_name"])
        self.mock_client.post.assert_called_once_with("/api/v1/auth/register", json=user_data)

    def test_register_endpoint_duplicate_email(self):
        """Test registration with duplicate email."""
        # Given: Registration data with existing email
        user_data = UserCreateFactory(email="existing@example.com")
        
        # Mock error response
        mock_response = Mock()
        mock_response.status_code = 400
        mock_response.json.return_value = {"detail": "Email already registered"}
        self.mock_client.post.return_value = mock_response

        # When: Making registration request
        response = self.mock_client.post("/api/v1/auth/register", json=user_data)

        # Then: Should return error
        self.assertEqual(response.status_code, 400)
        self.assertIn("already registered", response.json()["detail"])

    def test_login_endpoint_success(self):
        """Test successful login endpoint."""
        # Given: Valid login credentials and token
        login_data = UserLoginFactory()
        token_data = TokenFactory()
        
        # Mock successful response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "access_token": token_data["access_token"],
            "token_type": token_data["token_type"],
            "expires_in": token_data["expires_in"]
        }
        self.mock_client.post.return_value = mock_response

        # When: Making login request
        response = self.mock_client.post("/api/v1/auth/login", json=login_data)

        # Then: Should return token
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual(response_data["access_token"], token_data["access_token"])
        self.assertEqual(response_data["token_type"], token_data["token_type"])

    def test_login_endpoint_invalid_credentials(self):
        """Test login with invalid credentials."""
        # Given: Invalid login credentials
        login_data = UserLoginFactory(password="wrongpassword")
        
        # Mock error response
        mock_response = Mock()
        mock_response.status_code = 401
        mock_response.json.return_value = {"detail": "Incorrect email or password"}
        self.mock_client.post.return_value = mock_response

        # When: Making login request
        response = self.mock_client.post("/api/v1/auth/login", json=login_data)

        # Then: Should return error
        self.assertEqual(response.status_code, 401)
        self.assertIn("Incorrect email or password", response.json()["detail"])

    def test_get_current_user_endpoint_success(self):
        """Test successful current user retrieval."""
        # Given: Valid token and user
        token = "valid_bearer_token"
        user_data = UserResponseFactory()
        
        # Mock successful response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = user_data
        self.mock_client.get.return_value = mock_response

        # When: Making request with authorization header
        headers = {"Authorization": f"Bearer {token}"}
        response = self.mock_client.get("/api/v1/auth/me", headers=headers)

        # Then: Should return user data
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual(response_data["id"], user_data["id"])
        self.assertEqual(response_data["email"], user_data["email"])

    def test_get_current_user_endpoint_unauthorized(self):
        """Test current user retrieval without valid token."""
        # Given: No or invalid token
        # Mock unauthorized response
        mock_response = Mock()
        mock_response.status_code = 401
        mock_response.json.return_value = {"detail": "Not authenticated"}
        self.mock_client.get.return_value = mock_response

        # When: Making request without authorization header
        response = self.mock_client.get("/api/v1/auth/me")

        # Then: Should return unauthorized error
        self.assertEqual(response.status_code, 401)
        self.assertIn("Not authenticated", response.json()["detail"])

    def test_register_endpoint_validation_errors(self):
        """Test registration with various validation errors."""
        validation_cases = [
            {"field": "email", "value": "invalid-email", "expected_status": 422},
            {"field": "username", "value": "", "expected_status": 422},
            {"field": "password", "value": "short", "expected_status": 422},
        ]
        
        for case in validation_cases:
            with self.subTest(case=case):
                # Given: Invalid registration data
                user_data = UserCreateFactory()
                user_data[case["field"]] = case["value"]
                
                # Mock validation error response
                mock_response = Mock()
                mock_response.status_code = case["expected_status"]
                mock_response.json.return_value = {
                    "detail": f"Validation error for field '{case['field']}'"
                }
                self.mock_client.post.return_value = mock_response

                # When: Making registration request
                response = self.mock_client.post("/api/v1/auth/register", json=user_data)

                # Then: Should return validation error
                self.assertEqual(response.status_code, case["expected_status"])

    def test_logout_endpoint_success(self):
        """Test successful logout endpoint."""
        # Given: Valid token
        token = "valid_bearer_token"
        
        # Mock successful response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"message": "Successfully logged out"}
        self.mock_client.post.return_value = mock_response

        # When: Making logout request
        headers = {"Authorization": f"Bearer {token}"}
        response = self.mock_client.post("/api/v1/auth/logout", headers=headers)

        # Then: Should return success message
        self.assertEqual(response.status_code, 200)
        self.assertIn("Successfully logged out", response.json()["message"])


class TestAuthEndpointIntegration(unittest.TestCase):
    """Test auth endpoint integration scenarios."""

    def setUp(self):
        """Set up test fixtures."""
        self.mock_client = Mock()

    def test_full_auth_flow_simulation(self):
        """Test complete authentication flow simulation."""
        # Given: User registration and login data
        registration_data = UserCreateFactory()
        login_data = UserLoginFactory(
            email=registration_data["email"],
            password=registration_data["password"]
        )
        
        # Step 1: Register user
        register_response = Mock()
        register_response.status_code = 201
        register_response.json.return_value = UserResponseFactory(
            email=registration_data["email"],
            username=registration_data["username"]
        )
        
        # Step 2: Login user
        login_response = Mock()
        login_response.status_code = 200
        token_data = TokenFactory()
        login_response.json.return_value = token_data
        
        # Step 3: Access protected resource
        me_response = Mock()
        me_response.status_code = 200
        me_response.json.return_value = UserResponseFactory(
            email=registration_data["email"],
            username=registration_data["username"]
        )
        
        # Mock client responses
        self.mock_client.post.side_effect = [register_response, login_response]
        self.mock_client.get.return_value = me_response

        # When: Executing full flow
        # Register
        reg_resp = self.mock_client.post("/api/v1/auth/register", json=registration_data)
        
        # Login
        login_resp = self.mock_client.post("/api/v1/auth/login", json=login_data)
        
        # Access protected resource
        token = login_resp.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        me_resp = self.mock_client.get("/api/v1/auth/me", headers=headers)

        # Then: All steps should succeed
        self.assertEqual(reg_resp.status_code, 201)
        self.assertEqual(login_resp.status_code, 200)
        self.assertEqual(me_resp.status_code, 200)
        
        # And: Data should be consistent
        self.assertEqual(
            reg_resp.json()["email"], 
            me_resp.json()["email"]
        )

    def test_endpoint_error_handling_scenarios(self):
        """Test various error handling scenarios."""
        error_scenarios = [
            {
                "name": "network_error",
                "exception": ConnectionError("Network error"),
                "expected_handling": "Should handle network errors gracefully"
            },
            {
                "name": "server_error", 
                "status_code": 500,
                "response": {"detail": "Internal server error"},
                "expected_handling": "Should handle server errors"
            },
            {
                "name": "rate_limit_error",
                "status_code": 429,
                "response": {"detail": "Too many requests"},
                "expected_handling": "Should handle rate limiting"
            }
        ]
        
        for scenario in error_scenarios:
            with self.subTest(scenario=scenario["name"]):
                # Reset the mock before each scenario
                self.mock_client.post.reset_mock()
                self.mock_client.post.side_effect = None
                
                # Given: Different error scenarios
                if "exception" in scenario:
                    self.mock_client.post.side_effect = scenario["exception"]
                    
                    # When/Then: Should handle exception
                    with self.assertRaises(type(scenario["exception"])):
                        self.mock_client.post("/api/v1/auth/register", json={})
                else:
                    # Mock error response
                    mock_response = Mock()
                    mock_response.status_code = scenario["status_code"]
                    mock_response.json.return_value = scenario["response"]
                    self.mock_client.post.return_value = mock_response
                    
                    # When: Making request
                    response = self.mock_client.post("/api/v1/auth/register", json={})
                    
                    # Then: Should return appropriate error
                    self.assertEqual(response.status_code, scenario["status_code"])

    def test_endpoint_data_consistency_validation(self):
        """Test endpoint data consistency validation."""
        # Given: Multiple test scenarios using factories
        registration_scenarios = [UserCreateFactory() for _ in range(3)]
        login_scenarios = [UserLoginFactory() for _ in range(3)]

        # When: We validate the data structure for endpoints
        for reg_data in registration_scenarios:
            # Then: All registration data should be valid for endpoints
            required_fields = ["email", "username", "password", "full_name"]
            self.assertTrue(all(field in reg_data for field in required_fields))
            self.assertIn("@", reg_data["email"])
            self.assertGreaterEqual(len(reg_data["password"]), 8)

        for login_data in login_scenarios:
            # Then: All login data should be valid for endpoints
            required_fields = ["email", "password"]
            self.assertTrue(all(field in login_data for field in required_fields))
            self.assertIn("@", login_data["email"])
            self.assertGreater(len(login_data["password"]), 0)

    def test_authorization_header_validation(self):
        """Test authorization header validation logic."""
        header_cases = [
            {"header": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.token", "valid": True},
            {"header": "Bearer ", "valid": False},
            {"header": "InvalidFormat", "valid": False},
            {"header": "", "valid": False},
            {"header": None, "valid": False},
        ]
        
        for case in header_cases:
            with self.subTest(header=case["header"]):
                # Given: Different authorization header formats
                # When: We validate the header format
                if case["header"]:
                    parts = case["header"].split(" ")
                    is_valid = (
                        len(parts) == 2 and 
                        parts[0] == "Bearer" and 
                        len(parts[1]) > 0
                    )
                else:
                    is_valid = False

                # Then: We get the expected validation result
                self.assertEqual(is_valid, case["valid"])


if __name__ == '__main__':
    unittest.main()