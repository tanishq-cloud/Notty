import asyncio
import httpx
from fastapi import status
from schemas.user import UserCreateDTO, RefreshTokenDTO

BASE_URL = "http://192.168.0.193:8000"

TEST_USER = {
    "username": "testuser34",
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
        assert response.status_code == status.HTTP_200_OK, f"Failed to register user, got {response.status_code}"
        assert response.json() == {"message": "User created successfully"}, f"Unexpected response: {response.json()}"

async def login_and_get_tokens():
    """Test user login and token generation."""
    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        response = await client.post(
            "/token/",
            data={"username": TEST_USER["username"], "password": TEST_USER["password"]}
        )
        assert response.status_code == status.HTTP_200_OK, f"Login failed, got {response.status_code}"
        tokens = response.json()
        assert "access_token" in tokens, "No access_token found in the response"
        assert "refresh_token" in tokens, "No refresh_token found in the response"
        assert tokens["token_type"] == "bearer", "Token type is not 'bearer'"
        return tokens

async def refresh_access_token(refresh_token):
    """Test refreshing an access token."""
    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        response = await client.post(
            "/refresh/",
            json=RefreshTokenDTO(refresh_token=refresh_token).dict()
        )
        assert response.status_code == status.HTTP_200_OK, f"Failed to refresh token, got {response.status_code}"
        new_tokens = response.json()
        assert "access_token" in new_tokens, "No new access_token found"
        assert new_tokens["token_type"] == "bearer", "Token type is not 'bearer'"

async def run_tests():
    """Run all tests sequentially."""
    try:
        await register_user()
        tokens = await login_and_get_tokens()
        await refresh_access_token(tokens["refresh_token"])

        print("All tests passed!")
    except AssertionError as e:
        print(f"Test failed: {e}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    asyncio.run(run_tests())
