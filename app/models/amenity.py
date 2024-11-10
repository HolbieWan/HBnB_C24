# amenity.py

from app.models.base_model import BaseModel
from app.extensions import db

class Amenity(BaseModel):
    __tablename__ = 'amenities'
    name = db.Column(db.String(50), nullable=False)