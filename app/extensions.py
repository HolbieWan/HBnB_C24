from flask_bcrypt import Bcrypt # type: ignore
from flask_jwt_extended import JWTManager # type: ignore
from flask_sqlalchemy import SQLAlchemy # type: ignore

bcrypt = Bcrypt()
jwt = JWTManager()
db = SQLAlchemy()