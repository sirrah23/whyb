from flask import request
from flask_jwt import JWT
from whyb_backend import app, bcrypt, db
from whyb_backend.models import User


def authenticate(username, password):
    user = User.query.filter_by(username=username).first()
    if user and bcrypt.check_password_hash(user.password, password):
        return user

def identity(payload):
    user_id = payload['identity']
    return User.query.filter_by(id=user_id).first()

jwt = JWT(app, authenticate, identity)

@app.route('/register', methods=['POST'])
def register():
    content = request.json
    if (not 'username' in content) or (not 'password' in content):
        return 'Missing username or password', 400
    user = User.query.filter_by(username=content['username']).first()
    if user:
        return 'Username is taken', 400
    hashed_password = bcrypt.generate_password_hash(content['password'])
    user = User(username=content['username'], password=hashed_password) 
    db.session.add(user)
    db.session.commit()
    return '', 201
