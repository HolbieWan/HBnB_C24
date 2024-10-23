from base_test import BaseTestClass

class TestReviewEndpoints(BaseTestClass):

    def test_create_review(self):
        """Test creating a new review successfully"""
        response = self.client.post('/api/v1/reviews/', json={
            "comment": "Great place to stay!",
            "rating": 5,
            "user_id": self.owner_id,  # Reusing the user created in BaseTestClass
            "place_id": self.place_id   # Reusing the place created in BaseTestClass
        })
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertIn('comment', data)
        self.assertEqual(data['comment'], 'Great place to stay!')

    def test_get_all_reviews(self):
        """Test retrieving all reviews"""
        # Create a review first to make sure there's data
        self.client.post('/api/v1/reviews/', json={
            "comment": "Nice apartment",
            "rating": 4,
            "user_id": self.owner_id,
            "place_id": self.place_id
        })
        response = self.client.get('/api/v1/reviews/')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertGreaterEqual(len(data), 1)
        self.assertIn('comment', data[0])

    def test_get_review_by_id(self):
        """Test retrieving a review by ID"""
        # First create a review
        response = self.client.post('/api/v1/reviews/', json={
            "comment": "Nice apartment",
            "rating": 4,
            "user_id": self.owner_id,
            "place_id": self.place_id
        })
        review_id = response.get_json()['id']

        # Now get the review by ID
        response = self.client.get(f'/api/v1/reviews/{review_id}')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['comment'], 'Nice apartment')

    def test_get_review_by_id_not_found(self):
        """Test retrieving a review with a non-existent ID"""
        response = self.client.get('/api/v1/reviews/nonexistent-id')
        self.assertEqual(response.status_code, 404)
        self.assertIn('Review not found', response.get_json()['error'])

    def test_update_review(self):
        """Test updating a review's information"""
        # First create a review to update
        response = self.client.post('/api/v1/reviews/', json={
            "comment": "Average stay",
            "rating": 3,
            "user_id": self.owner_id,
            "place_id": self.place_id
        })
        review_id = response.get_json()['id']

        # Now update the review
        response = self.client.put(f'/api/v1/reviews/{review_id}', json={
            "comment": "Good stay",
            "rating": 4
        })
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['comment'], 'Good stay')
        self.assertEqual(data['rating'], 4)

    def test_update_review_not_found(self):
        """Test updating a review with a non-existent ID"""
        response = self.client.put('/api/v1/reviews/nonexistent-id', json={
            "comment": "Not found",
            "rating": 1
        })
        self.assertEqual(response.status_code, 404)
        self.assertIn('Review not found', response.get_json()['error'])

    def test_delete_review(self):
        """Test deleting a review by ID"""
        # First create a review to delete
        response = self.client.post('/api/v1/reviews/', json={
            "comment": "Short stay",
            "rating": 2,
            "user_id": self.owner_id,
            "place_id": self.place_id
        })
        review_id = response.get_json()['id']

        # Now delete the review
        response = self.client.delete(f'/api/v1/reviews/{review_id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn(f'Review {review_id} deleted successfully', response.get_json()['message'])

    def test_delete_review_not_found(self):
        """Test deleting a review with a non-existent ID"""
        response = self.client.delete('/api/v1/reviews/nonexistent-id')
        self.assertEqual(response.status_code, 404)
        self.assertIn('Review not found', response.get_json()['error'])