import unittest
from app import create_app
import uuid


class TestUserEndpoints(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = create_app()
        cls.client = cls.app.test_client()

        cls.app_context = cls.app.app_context()
        cls.app_context.push()

        # Create a unique admin user for this test class
        admin_email = f"admin_user_{uuid.uuid4()}@example.com"
        admin_data = {
            "first_name": "Admin",
            "last_name": "User",
            "email": admin_email,
            "password": "adminpass",
            "is_admin": True,
        }
        facade = cls.app.extensions['FACADE']
        cls.admin_user = facade.create_user(admin_data)

        # Log in as admin to get the access token
        login_data = {
            "email": admin_email,
            "password": "adminpass",
        }
        login_response = cls.client.post('/api/v1/login/', json=login_data)
        login_response_json = login_response.get_json()
        if login_response.status_code != 200 or not login_response_json:
            raise RuntimeError("Failed to log in as admin")
        cls.admin_token = login_response_json.get("access_token")

    @classmethod
    def tearDownClass(cls):
        facade = cls.app.extensions['FACADE']
        facade.delete_user(cls.admin_user.id)
        cls.app_context.pop()

    def test_get_users(self):
        """Test retrieving all users"""
        headers = {"Authorization": f"Bearer {self.admin_token}"}
        response = self.client.get('/api/v1/users/', headers=headers)
        response_json = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response_json, list)

    def test_create_user(self):
        """Test creating a user"""
        headers = {"Authorization": f"Bearer {self.admin_token}"}
        user_data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": f"john.doe_{uuid.uuid4()}@example.com",
            "password": "password123",
        }
        response = self.client.post('/api/v1/users/', json=user_data, headers=headers)
        response_json = response.get_json()
        self.assertEqual(response.status_code, 201)
        self.assertIn("id", response_json)
        self.assertEqual(response_json["first_name"], "John")
        self.assertEqual(response_json["last_name"], "Doe")

    def test_get_user_by_id(self):
        """Test retrieving a user by ID"""
        headers = {"Authorization": f"Bearer {self.admin_token}"}
        user_data = {
            "first_name": "Jane",
            "last_name": "Smith",
            "email": f"jane.smith_{uuid.uuid4()}@example.com",
            "password": "password123",
        }
        create_response = self.client.post('/api/v1/users/', json=user_data, headers=headers)
        create_response_json = create_response.get_json()
        user_id = create_response_json["id"]

        response = self.client.get(f'/api/v1/users/{user_id}', headers=headers)
        response_json = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_json["id"], user_id)
        self.assertEqual(response_json["first_name"], "Jane")
        self.assertEqual(response_json["last_name"], "Smith")

    def test_delete_user(self):
        """Test deleting a user"""
        headers = {"Authorization": f"Bearer {self.admin_token}"}
        user_data = {
            "first_name": "Mark",
            "last_name": "Lee",
            "email": f"mark.lee_{uuid.uuid4()}@example.com",
            "password": "password123",
        }
        create_response = self.client.post('/api/v1/users/', json=user_data, headers=headers)
        create_response_json = create_response.get_json()
        user_id = create_response_json["id"]

        delete_response = self.client.delete(f'/api/v1/users/{user_id}', headers=headers)
        delete_response_json = delete_response.get_json()
        self.assertEqual(delete_response.status_code, 200)
        self.assertEqual(delete_response_json["message"], f"User {user_id} deleted successfully")

        get_response = self.client.get(f'/api/v1/users/{user_id}', headers=headers)
        self.assertEqual(get_response.status_code, 404)

if __name__ == "__main__":
    unittest.main()