import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from whyb_backend import config


app = Flask(__name__)
config_type = os.environ.get('CONFIG_TYPE', '')
app.config.from_object(config.getConfigObject(config_type))

db = SQLAlchemy(app)
api = Api(app)
bcrypt = Bcrypt(app)
CORS(app)

from whyb_backend import auth
from whyb_backend import models
from whyb_backend import resources

db.create_all()
