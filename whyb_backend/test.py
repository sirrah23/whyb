import json
from flask_testing import TestCase
from whyb_backend import app, db, bcrypt
from whyb_backend.models import User
from whyb_backend.config import TestingConfig


def create_user(username, password):
    u1 = User(username=username, password=bcrypt.generate_password_hash(password))  # TODO: Remove this logic from testing code
    db.session.add(u1)
    db.session.commit()
    return u1


class BaseTestCase(TestCase):

    def create_app(self):
        #app.config.from_object(TestingConfig)
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()


class JWTTestCase(BaseTestCase):

    def test_valid_user_can_get_token(self):
        u1 = create_user('test1', 'password')
        response = self.client.post(
            '/auth',
            data=json.dumps({'username': 'test1', 'password': 'password'}),
            content_type="application/json")
        self.assert200(response)
        assert u'access_token' in response.json.keys()

    def test_invalid_user_cant_get_token(self):
        response = self.client.post(
            '/auth',
            data=json.dumps({'username': 'test2', 'password': 'password'}),
            content_type="application/json")
        self.assert401(response)


class LocationListTestCase(BaseTestCase):

    def _get_jwt_token(self, username, password):
        response = self.client.post(
            '/auth',
            data=json.dumps({'username': username, 'password': password}),
            content_type="application/json")
        return response.json['access_token']

    def test_create_location(self):
        u1 = create_user('test1', 'password')
        token = self._get_jwt_token('test1', 'password')
        response = self.client.post(
            '/locations',
            data=json.dumps({'name':'Location X', 'latitude': 0, 'longitude': 0}),
            content_type='application/json',
            headers={"Authorization":"JWT {}".format(token)})

        self.assertStatus(response, 201)
        data = response.json['data']
        assert 'id' in data.keys()
        assert data['name'] == 'Location X'
        assert int(data['latitude']) == 0
        assert int(data['longitude']) == 0

    def test_get_nonexistent_locations(self):
        u1 = create_user('test1', 'password')
        token = self._get_jwt_token('test1', 'password')
        response = self.client.get(
            '/locations',
            headers={"Authorization":"JWT {}".format(token)})
        self.assert200(response)
        assert len(response.json['data']) == 0

    def test_get_existent_locations(self):
        u1 = create_user('test1', 'password')
        token = self._get_jwt_token('test1', 'password')
        response_l1 = self.client.post(
            '/locations',
            data=json.dumps({'name':'Location X', 'latitude': 0, 'longitude': 0}),
            content_type='application/json',
            headers={"Authorization":"JWT {}".format(token)})
        response_l2 = self.client.post(
            '/locations',
            data=json.dumps({'name':'Location X', 'latitude': 0, 'longitude': 0}),
            content_type='application/json',
            headers={"Authorization":"JWT {}".format(token)})
        response_l3 = self.client.post(
            '/locations',
            data=json.dumps({'name':'Location X', 'latitude': 0, 'longitude': 0}),
            content_type='application/json',
            headers={"Authorization":"JWT {}".format(token)})
        response_ls = self.client.get(
            '/locations',
            headers={"Authorization":"JWT {}".format(token)})
        self.assert200(response_ls)
        ls = response_ls.json['data']
        assert response_l1.json['data']['id'] in ls
        assert response_l2.json['data']['id'] in ls
        assert response_l3.json['data']['id'] in ls

    def test_get_locations_different_user(self):
        u1 = create_user('test1', 'password')
        token1 = self._get_jwt_token('test1', 'password')
        u2 = create_user('test2', 'password')
        token2 = self._get_jwt_token('test2', 'password')
        response_u1 = self.client.post(
            '/locations',
            data=json.dumps({'name':'Location X', 'latitude': 0, 'longitude': 0}),
            content_type='application/json',
            headers={"Authorization":"JWT {}".format(token1)})
        response_u2 = self.client.post(
            '/locations',
            data=json.dumps({'name':'Location X', 'latitude': 0, 'longitude': 0}),
            content_type='application/json',
            headers={"Authorization":"JWT {}".format(token2)})
        response_get_u1 = self.client.get(
            '/locations',
            headers={"Authorization":"JWT {}".format(token1)})
        response_get_u2 = self.client.get(
            '/locations',
            headers={"Authorization":"JWT {}".format(token2)})


        self.assert200(response_get_u1)
        assert len(response_get_u1.json['data']) == 1
        assert response_get_u1.json['data'][0] == response_u1.json['data']['id']

        self.assert200(response_get_u2)
        assert len(response_get_u2.json['data']) == 1
        assert response_get_u2.json['data'][0] == response_u2.json['data']['id']


class LocationTestCase(BaseTestCase):

    def _get_jwt_token(self, username, password):
        response = self.client.post(
            '/auth',
            data=json.dumps({'username': username, 'password': password}),
            content_type="application/json")
        return response.json['access_token']

    def test_get_location(self):
        u1 = create_user('test1', 'password')
        token = self._get_jwt_token('test1', 'password')
        response_create = self.client.post(
            '/locations',
            data=json.dumps({'name':'Location X', 'latitude': 0, 'longitude': 0}),
            content_type='application/json',
            headers={"Authorization":"JWT {}".format(token)})
        response_get = self.client.get(
            '/location/{}'.format(response_create.json['data']['id']),
            headers={'Authorization': 'JWT {}'.format(token)})
        data_create = response_create.json['data']
        data_get = response_get.json['data']

        self.assert200(response_get)
        assert data_get['id'] == data_create['id']
        assert data_get['name'] == 'Location X'
        assert int(data_get['latitude']) == 0
        assert int(data_get['longitude']) == 0

    def test_delete_location(self):
        u1 = create_user('test1', 'password')
        token = self._get_jwt_token('test1', 'password')
        response_create = self.client.post(
            '/locations',
            data=json.dumps({'name':'Location X', 'latitude': 0, 'longitude': 0}),
            content_type='application/json',
            headers={"Authorization":"JWT {}".format(token)})
        response_get_1 = self.client.get(
            '/location/{}'.format(response_create.json['data']['id']),
            headers={'Authorization': 'JWT {}'.format(token)})
        response_delete = self.client.delete(
            '/location/{}'.format(response_create.json['data']['id']),
            headers={'Authorization': 'JWT {}'.format(token)})
        response_get_2 = self.client.get(
            '/location/{}'.format(response_create.json['data']['id']),
            headers={'Authorization': 'JWT {}'.format(token)})

        # Create succeeds
        self.assertStatus(response_create, 201)
        # Get succeeds
        self.assert200(response_get_1)
        # Delete succeeds
        self.assertStatus(response_delete, 204)
        # Get of deleted fails
        self.assert404(response_get_2)


class RegistrationTestCase(BaseTestCase):

    def test_successfull_registration(self):
        assert 0 == len(User.query.all())
        username = "test1"
        password = "password"
        res = self.client.post(
            '/register',
            data=json.dumps({'username': username, 'password': password}),
            content_type='application/json')
        self.assertStatus(res, 201)
        assert 1 == len(User.query.all())
        user = User.query.all()[0]
        assert user.username == username
        assert user.password != password  # Storing hashed password
        
    def test_failed_registration(self):
        assert 0 == len(User.query.all())
        username = "test1"
        password = "password"
        res = self.client.post(
            '/register',
            data=json.dumps({'username': username, 'password': password}),
            content_type='application/json')
        self.assertStatus(res, 201)
        assert 1 == len(User.query.all())
        user = User.query.all()[0]
        assert user.username == username
        assert user.password != password  # Storing hashed password

        res = self.client.post(
            '/register',
            data=json.dumps({'username': username, 'password': password}),
            content_type='application/json')
        self.assert400(res)  # User already exists
        