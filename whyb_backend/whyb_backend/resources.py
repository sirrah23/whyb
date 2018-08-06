from flask_restful import Resource, reqparse
from flask_jwt import jwt_required, current_identity
from whyb_backend import api, db
from whyb_backend.models import Location


class LocationListResource(Resource):

    decorators = [jwt_required()]

    def get(self):
        user = current_identity
        location_ids = [location.id for location in user.locations]
        return {'message':'Success', 'data': location_ids}, 200

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', required=True)
        parser.add_argument('latitude', required=True)
        parser.add_argument('longitude', required=True)
        args = parser.parse_args()
        user_id = current_identity.id

        location = Location(
            name=args.name,
            latitude=args.latitude,
            longitude=args.longitude,
            user_id=user_id)

        db.session.add(location)
        db.session.commit()

        args.id = location.id
        return {'message':'Success', 'data': args}, 201


class LocationResource(Resource):

    decorators = [jwt_required()]

    @staticmethod
    def userHasAccess(location, user_id):
        return location.user_id == user_id

    def get(self, location_id):
        user_id = current_identity.id
        location = Location.query.get(location_id)
        if not location:
            return {'message': 'Location not found', 'data': {}}, 404
        if not LocationResource.userHasAccess(location, user_id):
            return {'message': 'Access to this location is not authorized', "data": {}}, 401
        return {
            'message': 'Success',
            'data': {
                'id': location.id,
                'name': location.name,
                'latitude': location.latitude,
                'longitude': location.longitude
            }
        }, 200

    def delete(self, location_id):
        user_id = current_identity.id
        location = Location.query.get(location_id)
        if not location:
            return {'message': 'Location not found', 'data': {}}, 404
        if not LocationResource.userHasAccess(location, user_id):
            return {'message': 'Access to this location is not authorized', "data": {}}, 401
        db.session.delete(location)
        db.session.commit()
        return '', 204


api.add_resource(LocationListResource, '/locations')
api.add_resource(LocationResource, '/location/<int:location_id>')
