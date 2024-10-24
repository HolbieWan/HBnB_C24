from flask_restx import Namespace, Resource, fields
from flask import current_app


api = Namespace('reviews', description='Review operations')

# Define the review model for input validation and documentation
review_model = api.model('Review', {
    'comment': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True, description='Rating of the place (1-5)'),
    'user_id': fields.String(required=True, description='ID of the user'),
    'place_id': fields.String(required=True, description='ID of the place')
})


@api.route('/')
class ReviewList(Resource):
    @api.expect(review_model)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new review"""
        facade = current_app.facade # type: ignore
        review_data = api.payload

        # Validate required fields
        if not all(key in review_data for key in ('user_id', 'place_id', 'rating', 'comment')):
            return {'error': 'Missing required fields'}, 400

        # Validate user and place exist
        user = facade.get_user(review_data['user_id'])
        if not user:
            return {'error': 'User not found'}, 400

        place = facade.get_place(review_data['place_id'])
        if not place:
            return {'error': 'Place not found'}, 400

        try:
            new_review = facade.create_review(review_data)
        except ValueError as e:
            return {'error': str(e)}, 400

        return {
            'id': new_review.id,
            'comment': new_review.comment,
            'rating': new_review.rating,
            'user_id': new_review.user_id,
            'place_id': new_review.place_id
        }, 201

    @api.response(200, 'List of reviews retrieved successfully')
    def get(self):
        """Retrieve a list of all reviews"""
        facade = current_app.facade # type: ignore
        reviews = facade.get_all_reviews()
        review_list = []
        for review in reviews:
            review_list.append({
                'id': review.id,
                'comment': review.comment,
                'rating': review.rating,
                'user_id': review.user_id,
                'place_id': review.place_id
            })
        return review_list, 200

@api.route('/<review_id>')
class ReviewResource(Resource):
    @api.response(200, 'Review details retrieved successfully')
    @api.response(404, 'Review not found')
    def get(self, review_id):
        """Get review details by ID"""
        facade = current_app.facade # type: ignore
        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404
        return {
            'id': review.id,
            'comment': review.comment,
            'rating': review.rating,
            'user_id': review.user_id,
            'place_id': review.place_id
        }, 200

    @api.expect(review_model)
    @api.response(200, 'Review updated successfully')
    @api.response(404, 'Review not found')
    @api.response(400, 'Invalid input data')
    def put(self, review_id):
        """Update a review's information"""
        facade = current_app.facade # type: ignore
        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404

        review_data = api.payload

        try:
            facade.update_review(review_id, review_data)
        except ValueError as e:
            return {'error': str(e)}, 400

        updated_review = facade.get_review(review_id)
        return {
            'id': updated_review.id,
            'comment': updated_review.comment,
            'rating': updated_review.rating,
            'user_id': updated_review.user_id,
            'place_id': updated_review.place_id
        }, 200

    @api.response(200, 'Review deleted successfully')
    @api.response(404, 'Review not found')
    def delete(self, review_id):
        """Delete a review"""
        facade = current_app.facade # type: ignore
        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404

        facade.delete_review(review_id)
        return {'message': f'Review {review_id} deleted successfully'}, 200

@api.route('/places/<place_id>/reviews')
class PlaceReviewList(Resource):
    @api.response(200, 'List of reviews for the place retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get all reviews for a specific place"""
        facade = current_app.facade # type: ignore
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404

        reviews = facade.get_reviews_by_place(place_id)
        reviews_list = []
        for review in reviews:
            reviews_list.append({
                'id': review.id,
                'comment': review.comment,
                'rating': review.rating,
                'user_id': review.user_id,
                'place_id': review.place_id
            })
        return reviews_list, 200