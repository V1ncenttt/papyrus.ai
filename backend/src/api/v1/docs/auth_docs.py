signup_docs = {
    "summary": "User Signup",
    "description": "Create a new user account by providing a username, email, and password. This endpoint returns a success message upon successful account creation.",
    "responses": {
        200: {"description": "User signed up successfully"},
        400: {"description": "Invalid input"},
    },
}

login_docs = {
    "summary": "User Login",
    "description": "Authenticate a user by providing a username and password. This endpoint returns a JWT token upon successful authentication.",
    "responses": {
        200: {"description": "User logged in successfully"},
        401: {"description": "Invalid credentials"},
    },
}
