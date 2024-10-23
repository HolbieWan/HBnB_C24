from base_test import BaseTestClass

class TestUserEndpoints(BaseTestClass):

    def test_create_user(self):
        """Test creating a new user successfully"""
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "jane.doe@gmail.com"
        })
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertIn('first_name', data)
        self.assertEqual(data['first_name'], 'Jane')

    def test_get_all_users(self):
        """Test retrieving all users"""
        response = self.client.get('/api/v1/users/')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertGreaterEqual(len(data), 1)
        self.assertIn('email', data[0])

    def test_get_user_by_id(self):
        """Test retrieving a user by ID"""
        # First create a user
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Alice",
            "last_name": "Smith",
            "email": "alice.smith@gmail.com"
        })
        user_id = response.get_json()['id']

        # Now get the user by ID
        response = self.client.get(f'/api/v1/users/{user_id}')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['first_name'], 'Alice')

    def test_get_user_by_id_not_found(self):
        """Test retrieving a user with a non-existent ID"""
        response = self.client.get('/api/v1/users/nonexistent-id')
        self.assertEqual(response.status_code, 404)
        self.assertIn('User not found', response.get_json()['error'])

    def test_delete_user(self):
        """Test deleting a user by ID"""
        # First create a user to delete
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Bob",
            "last_name": "Jones",
            "email": "bob.jones@gmail.com"
        })
        user_id = response.get_json()['id']

        # Now delete the user
        response = self.client.delete(f'/api/v1/users/{user_id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn(f'User {user_id} deleted successfully', response.get_json()['message'])

    def test_delete_user_not_found(self):
        """Test deleting a user with a non-existent ID"""
        response = self.client.delete('/api/v1/users/nonexistent-id')
        self.assertEqual(response.status_code, 404)
        self.assertIn('User not found', response.get_json()['error'])