import unittest
from app import create_app

class BaseTestClass(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.app = create_app()
        cls.client = cls.app.test_client()

        # Create a shared user to use as owner for all places
        response = cls.client.post('/api/v1/users/', json={
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@gmail.com"
        })
        cls.owner_id = response.get_json()['id']

        # Create some shared amenities
        response1 = cls.client.post('/api/v1/amenities/', json={"name": "Pool"})
        cls.amenity1_id = response1.get_json()['id']

        response2 = cls.client.post('/api/v1/amenities/', json={"name": "Wi-Fi"})
        cls.amenity2_id = response2.get_json()['id']