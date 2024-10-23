from flask_restx import Namespace, Resource, fields
from flask import current_app


api = Namespace('amenities', description='Amenity operations')

# Define the amenity model for input validation and documentation
amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Name of the amenity')
})


@api.route('/')
class AmenityList(Resource):
    @api.expect(amenity_model)
    @api.response(201, 'Amenity successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new amenity"""
        facade = current_app.facade # type: ignore
        amenity_data = api.payload

        if not amenity_data.get('name'):
            return {'error': 'Amenity name is required'}, 400

        new_amenity = facade.create_amenity(amenity_data)
        return {
            'id': new_amenity.id,
            'name': new_amenity.name
        }, 201

    @api.response(200, 'List of amenities retrieved successfully')
    def get(self):
        """Retrieve a list of all amenities"""
        facade = current_app.facade # type: ignore
        amenities = facade.get_all_amenities()
        amenity_list = []
        for amenity in amenities:
            amenity_list.append({
                'id': amenity.id,
                'name': amenity.name
            })
        return amenity_list, 200

@api.route('/<amenity_id>')
class AmenityResource(Resource):
    @api.response(200, 'Amenity details retrieved successfully')
    @api.response(404, 'Amenity not found')
    def get(self, amenity_id):
        """Get amenity details by ID"""
        facade = current_app.facade # type: ignore
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {'error': 'Amenity not found'}, 404
        return {
            'id': amenity.id,
            'name': amenity.name
        }, 200

    @api.expect(amenity_model)
    @api.response(200, 'Amenity updated successfully')
    @api.response(404, 'Amenity not found')
    @api.response(400, 'Invalid input data')
    def put(self, amenity_id):
        """Update an amenity's information"""
        facade = current_app.facade # type: ignore
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {'error': 'Amenity not found'}, 404

        amenity_data = api.payload
        if not amenity_data.get('name'):
            return {'error': 'Amenity name is required'}, 400

        facade.update_amenity(amenity_id, amenity_data)
        updated_amenity = facade.get_amenity(amenity_id)
        return {
            'id': updated_amenity.id,
            'name': updated_amenity.name
        }, 200