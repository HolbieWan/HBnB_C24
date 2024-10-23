from base_test import BaseTestClass

class TestPlaceEndpoints(BaseTestClass):

    def test_create_place(self):
        """Test creating a new place successfully"""
        response = self.client.post('/api/v1/places/', json={
            "title": "Beautiful Apartment",
            "description": "A cozy apartment in the city center",
            "price": 100.0,
            "latitude": 48.8566,
            "longitude": 2.3522,
            "owner_id": self.owner_id,
            "amenities": [self.amenity1_id, self.amenity2_id]
        })
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertIn('title', data)
        self.assertEqual(data['title'], 'Beautiful Apartment')

    def test_get_all_places(self):
        """Test retrieving all places"""
        response = self.client.get('/api/v1/places/')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertGreaterEqual(len(data), 1)
        self.assertIn('title', data[0])

    def test_get_place_by_id(self):
        """Test retrieving a place by its ID"""
        # First create a place
        response = self.client.post('/api/v1/places/', json={
            "title": "Luxury Villa",
            "description": "A luxurious villa with a pool",
            "price": 500.0,
            "latitude": 45.4215,
            "longitude": -75.6903,
            "owner_id": self.owner_id,
            "amenities": [self.amenity1_id]
        })
        place_id = response.get_json()['id']

        # Now get the place by ID
        response = self.client.get(f'/api/v1/places/{place_id}')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['title'], 'Luxury Villa')

    def test_get_place_by_id_not_found(self):
        """Test retrieving a place with a non-existent ID"""
        response = self.client.get('/api/v1/places/nonexistent-id')
        self.assertEqual(response.status_code, 404)
        self.assertIn('Place not found', response.get_json()['error'])

    def test_update_place(self):
        """Test updating a place's information"""
        # First create a place to update
        response = self.client.post('/api/v1/places/', json={
            "title": "Small Cottage",
            "description": "A small, cozy cottage",
            "price": 50.0,
            "latitude": 52.5200,
            "longitude": 13.4050,
            "owner_id": self.owner_id,
            "amenities": [self.amenity1_id]
        })
        place_id = response.get_json()['id']

        # Now update the place
        response = self.client.put(f'/api/v1/places/{place_id}', json={
            "title": "Updated Cottage",
            "description": "An updated cozy cottage",
            "price": 60.0,
            "amenities": [self.amenity2_id]
        })
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['title'], 'Updated Cottage')
        self.assertEqual(data['price'], 60.0)

    def test_update_place_not_found(self):
        """Test updating a place with a non-existent ID"""
        response = self.client.put('/api/v1/places/nonexistent-id', json={
            "title": "Nonexistent Place",
            "price": 99.0
        })
        self.assertEqual(response.status_code, 404)
        self.assertIn('Place not found', response.get_json()['error'])

    def test_delete_place(self):
        """Test deleting a place by ID"""
        # First create a place to delete
        response = self.client.post('/api/v1/places/', json={
            "title": "Beach House",
            "description": "A lovely beach house",
            "price": 200.0,
            "latitude": 36.7783,
            "longitude": -119.4179,
            "owner_id": self.owner_id,
            "amenities": [self.amenity1_id]
        })
        place_id = response.get_json()['id']

        # Now delete the place
        response = self.client.delete(f'/api/v1/places/{place_id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn(f'Place {place_id} deleted successfully', response.get_json()['message'])

    def test_delete_place_not_found(self):
        """Test deleting a place with a non-existent ID"""
        response = self.client.delete('/api/v1/places/nonexistent-id')
        self.assertEqual(response.status_code, 404)
        self.assertIn('Place not found', response.get_json()['error'])