import unittest
from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient
from main import app
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from models.model import User

DATABASE_URL = "sqlite:///:memory:"  

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def create_test_db():
    Base.metadata.create_all(bind=engine)

create_test_db()

class TestUserRoutes(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)
        create_test_db()

    def setUp(self):
        self.mock_db = MagicMock(spec=SessionLocal)        

    @patch("dao.user_dao.UserDAO.create_user")
    def test_create_user(self, mock_create_user):
        mock_create_user.return_value = {"username": "User341", "password": "hashedpassword", "full_name": "Test User"}
        
        user_data = {"username": "User341", "password": "password123", "full_name": "Test User"}
        
        response = self.client.post("/register/", json=user_data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "User created successfully"})

    @patch("dao.user_dao.UserDAO.create_user")  
    def test_create_user_already_exists(self, mock_create_user):
        mock_create_user.return_value = None
        
        user_data = {"username": "existinguser", "password": "password123", "full_name": "Existing User"}
        
        response = self.client.post("/register/", json=user_data)

        self.assertEqual(response.status_code, 500)

    @patch("dao.user_dao.UserDAO.verify_refresh_token")
    @patch("dao.user_dao.UserDAO.create_access_token")
    def test_refresh_token(self, mock_create_access_token, mock_verify_refresh_token):
        mock_verify_refresh_token.return_value = {"user": "testuser"}
        mock_create_access_token.return_value = "newfakeaccesstoken"

        refresh_data = {"refresh_token": "fakerefreshtoken"}

        response = self.client.post("/refresh/", json=refresh_data)

        self.assertEqual(response.status_code, 200)
        self.assertIn("access_token", response.json())
        self.assertEqual(response.json()["token_type"], "bearer")

 
if __name__ == "__main__":
    unittest.main()
