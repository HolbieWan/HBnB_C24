from base_test import BaseTestClass

class TestAmenityEndpoints(BaseTestClass):

    def test_create_amenity(self):
        """Test creating a new amenity successfully"""
        response = self.client.post('/api/v1/amenities/', json={
            "name": "Swimming Pool"
        })
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertIn('name', data)
        self.assertEqual(data['name'], 'Swimming Pool')

    def test_get_all_amenities(self):
        """Test retrieving all amenities"""
        response = self.client.get('/api/v1/amenities/')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertGreaterEqual(len(data), 1)
        self.assertIn('name', data[0])

    def test_get_amenity_by_id(self):
        """Test retrieving an amenity by ID"""
        # First create an amenity
        response = self.client.post('/api/v1/amenities/', json={
            "name": "Gym"
        })
        amenity_id = response.get_json()['id']

        # Now get the amenity by ID
        response = self.client.get(f'/api/v1/amenities/{amenity_id}')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['name'], 'Gym')

    def test_get_amenity_by_id_not_found(self):
        """Test retrieving an amenity with a non-existent ID"""
        response = self.client.get('/api/v1/amenities/nonexistent-id')
        self.assertEqual(response.status_code, 404)
        self.assertIn('Amenity not found', response.get_json()['error'])

    def test_update_amenity(self):
        """Test updating an amenity's information"""
        # First create an amenity to update
        response = self.client.post('/api/v1/amenities/', json={
            "name": "Spa"
        })
        amenity_id = response.get_json()['id']

        # Now update the amenity
        response = self.client.put(f'/api/v1/amenities/{amenity_id}', json={
            "name": "Luxury Spa"
        })
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['name'], 'Luxury Spa')

    def test_update_amenity_not_found(self):
        """Test updating an amenity with a non-existent ID"""
        response = self.client.put('/api/v1/amenities/nonexistent-id', json={
            "name": "Nonexistent Amenity"
        })
        self.assertEqual(response.status_code, 404)
        self.assertIn('Amenity not found', response.get_json()['error'])

    def test_delete_amenity(self):
        """Test deleting an amenity by ID"""
        # First create an amenity to delete
        response = self.client.post('/api/v1/amenities/', json={
            "name": "Game Room"
        })
        amenity_id = response.get_json()['id']

        # Now delete the amenity
        response = self.client.delete(f'/api/v1/amenities/{amenity_id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn(f'Place {amenity_id} deleted successfully', response.get_json()['message'])

    def test_delete_amenity_not_found(self):
        """Test deleting an amenity with a non-existent ID"""
        response = self.client.delete('/api/v1/amenities/nonexistent-id')
        self.assertEqual(response.status_code, 404)
        self.assertIn('Amenity not found', response.get_json()['error'])