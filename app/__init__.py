# __init__.py
from config import config
from flask import Flask
from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy # type: ignore
from app.api.v1.routes_users import api as users_ns
from app.api.v1.routes_places import api as places_ns
from app.api.v1.routes_amenities import api as amenities_ns
from app.api.v1.routes_reviews import api as reviews_ns
from app.api.v1.routes_login import api as login_ns

from app.services.facade import HBnBFacade
from app.extensions import bcrypt, jwt, db


def create_app(config_class="config.DevelopmentConfig"):
    app = Flask(__name__)
    app.config.from_object(config_class)
    api = Api(app, version='1.0', title='HBnB API', description='HBnB Application API')
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    facade = HBnBFacade() # type: ignore
    app.extensions['FACADE'] = facade

    # Register the users namespace
    api.add_namespace(users_ns, path='/api/v1/users')
    api.add_namespace(places_ns, path='/api/v1/places')
    api.add_namespace(amenities_ns, path='/api/v1/amenities')
    api.add_namespace(reviews_ns, path='/api/v1/reviews')
    api.add_namespace(login_ns, path='/api/v1/login')

    return app