import unittest
import uuid
from app import create_app


class TestReviewEndpoints(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = create_app()
        cls.client = cls.app.test_client()

        cls.app_context = cls.app.app_context()
        cls.app_context.push()

        facade = cls.app.extensions["FACADE"]

        # Create a unique admin user for this test class
        admin_email = f"admin_review_{uuid.uuid4()}@example.com"
        admin_data = {
            "first_name": "Admin",
            "last_name": "Reviewer",
            "email": admin_email,
            "password": "adminpass",
            "is_admin": True,
        }
        cls.admin_user = facade.create_user(admin_data)

        # Log in as admin
        login_response = cls.client.post(
            "/api/v1/login/",
            json={"email": admin_email, "password": "adminpass"},
        )
        cls.admin_token = login_response.get_json()["access_token"]

        # Create two regular users
        cls.user1_data = {
            "first_name": "User1",
            "last_name": "One",
            "email": f"user1_{uuid.uuid4()}@example.com",
            "password": "user1pass",
        }
        cls.user2_data = {
            "first_name": "User2",
            "last_name": "Two",
            "email": f"user2_{uuid.uuid4()}@example.com",
            "password": "user2pass",
        }
        cls.user1 = facade.create_user(cls.user1_data)
        cls.user2 = facade.create_user(cls.user2_data)

        # Log in as user2
        login_response = cls.client.post(
            "/api/v1/login/",
            json={"email": cls.user2_data["email"], "password": "user2pass"},
        )
        cls.user2_token = login_response.get_json()["access_token"]

    @classmethod
    def tearDownClass(cls):
        facade = cls.app.extensions["FACADE"]

        # Delete users
        facade.delete_user(cls.user1.id)
        facade.delete_user(cls.user2.id)
        facade.delete_user(cls.admin_user.id)
        cls.app_context.pop()

    def test_create_review(self):
        """Test creating a review successfully"""
        facade = self.app.extensions["FACADE"]
        place = facade.create_place({
            "title": "Test Place",
            "description": "Testing place",
            "price": 200.0,
            "latitude": 40.7128,
            "longitude": -74.0060,
            "owner_id": self.user1.id,
        })

        response = self.client.post(
            "/api/v1/reviews/",
            json={
                "text": "Amazing place!",
                "rating": 5,
                "user_id": self.user2.id,
                "place_id": place.id,
            },
            headers={"Authorization": f"Bearer {self.user2_token}"},
        )
        self.assertEqual(response.status_code, 201)

if __name__ == "__main__":
    unittest.main()