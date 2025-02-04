# # import pytest
# # from fastapi.testclient import TestClient
# # from main import app  # Adjust this import based on your app structure

# # @pytest.fixture
# # def client():
# #     with TestClient(app) as client:
# #         yield client

# # @pytest.mark.asyncio
# # async def test_create_note(client):
# #     note_data = {
# #         "username": "string12",
# #         "full_name":"string12",
# #         "password": "string1"
# #     }
# #     response = client.post("/register/", json=note_data)  
# #     assert response.status_code == 200
# #     response_data = response.json()
# #     login_data={"username":note_data['username'],"password":note_data['password']}
# #     response = client.post("/token/", data=login_data)  
# #     assert response.status_code == 200
# #     # assert response_data["title"] == note_data["title"]
# #     # assert response_data["body"] == note_data["body"]
# #     # # return response_data["id"]


# # test_create_note.py (Your test case)
# import pytest
# from fastapi.testclient import TestClient

# @pytest.mark.asyncio
# async def test_create_note(client):
#     # Register a user
#     note_data = {
#         "username": "string123445",
#         "full_name": "string1",
#         "password": "string1"
#     }
    
#     # Register the user
#     response = client.post("/register/", json=note_data)
#     assert response.status_code == 200
    
#     # Login to get the token
#     login_data = {
#         "username": note_data['username'],
#         "password": note_data['password']
#     }
#     response = client.post("/token/", data=login_data)  # Sending data as form data for OAuth2
#     assert response.status_code == 200
#     access_token = response.json().get("access_token")
#     assert access_token  # Ensure we received an access token

#     # Now that the user is authenticated, you can test other endpoints as needed


# test_create_note.py
import pytest

@pytest.mark.asyncio
async def test_create_note(client):
    note_data = {
        "username": "testuser1",
        "full_name": "Test User",
        "password": "password123"
    }
    # Register user
    # response = client.post("/register/", json=note_data)
    # assert response.status_code == 200

    # Login to get token
    login_data = {
        "username": note_data['username'],
        "password": note_data['password']
    }
    response = client.post("/token/", data=login_data)  # Send form data
    assert response.status_code == 200
    access_token = response.json().get("access_token")
    assert access_token  # Ensure we received an access token

    # Create a note
    note_data = {
        "title": "Test Note",
        "body": "This is a test note"
    }
    response = client.post("/note/", json=note_data, headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == 200
    note_id = response.json()["note_id"]
    assert note_id is not None

    # Get the created note
    response = client.get(f"/note/{note_id}", headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == 200
    note = response.json()
    assert note["title"] == note_data["title"]
    assert note["body"] == note_data["body"]
    client.close()
