import os
from flask import Flask
from flask_jwt import JWT, jwt_required, current_identity
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_restful import Resource, Api, reqparse
from werkzeug.security import safe_str_cmp
import config


# Create app
app = Flask(__name__)

# Configure app
config_type = os.environ.get('CONFIG_TYPE', '')
app.config.from_object(config.getConfigObject(config_type))

# Flask plugins
db = SQLAlchemy(app)
api = Api(app)
CORS(app)


# Database models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    locations = db.relationship('Location', backref='user', lazy=True)

    def __repr__(self):
        return "User({},{})".format(self.id, self.username)


class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return 'Location({},{},{},{})'.format(self.id, self.name, self.latitude, self.longitude)


# Create tables if they don't exist already
db.create_all()


# JSON Web Token authentication
def authenticate(username, password):
    user = User.query.filter_by(username=username).first()
    if user and safe_str_cmp(user.password.encode('utf-8'), password.encode('utf-8')):
        return user

def identity(payload):
    user_id = payload['identity']
    return User.query.filter_by(id=user_id).first()

jwt = JWT(app, authenticate, identity)

@app.route('/protected')
@jwt_required()
def protected():
    return '%s' % current_identity


# REST API resources
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


if __name__ == '__main__':
    app.run()
