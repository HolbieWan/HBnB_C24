# place.py

from app.models.base_model import BaseModel
from app.extensions import db

class Place(BaseModel):
    __tablename__ = 'places'
    title = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(1024), nullable=False)
    price = db.Column(db.Float, nullable=False, default=0)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    owner = db.Column(db.String(50), nullable=True)
    owner_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    reviews = db.Column(db.JSON, default=[])
    amenities = db.Column(db.JSON, default=[])