import asyncio
import httpx
from fastapi import status
from schemas.user import UserCreateDTO, RefreshTokenDTO

# Base URL of the FastAPI app (replace with your actual host)
BASE_URL = "http://127.0.0.1:8000"

# Test data
TEST_USER = {
    "username": "testuser",
    "password": "testpassword",
    "full_name": "Test User"
}

async def register_user():
    """Test user registration."""
    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        response = await client.post(
            "/register/",
            json=UserCreateDTO(**TEST_USER).dict()
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {"message": "User created successfully"}

async def login_and_get_tokens():
    """Test user login and token generation."""
    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        response = await client.post(
            "/token/",
            data={"username": TEST_USER["username"], "password": TEST_USER["password"]}
        )
        assert response.status_code == status.HTTP_200_OK
        tokens = response.json()
        assert "access_token" in tokens
        assert "refresh_token" in tokens
        assert tokens["token_type"] == "bearer"
        return tokens

async def refresh_access_token(refresh_token):
    """Test refreshing an access token."""
    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        response = await client.post(
            "/refresh/",
            json=RefreshTokenDTO(refresh_token=refresh_token).dict()
        )
        assert response.status_code == status.HTTP_200_OK
        new_tokens = response.json()
        assert "access_token" in new_tokens
        assert new_tokens["token_type"] == "bearer"

async def run_tests():
    """Run all tests sequentially."""
    try:
        # Step 1: Register a new user
        await register_user()

        # Step 2: Login and get tokens
        tokens = await login_and_get_tokens()

        # Step 3: Refresh the access token
        await refresh_access_token(tokens["refresh_token"])

        print("All tests passed!")
    except AssertionError as e:
        print(f"Test failed: {e}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    asyncio.run(run_tests())