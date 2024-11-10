# base_model.py

from app.extensions import db
import uuid
from datetime import datetime

class BaseModel(db.Model):
    __abstract__ = True  # This ensures SQLAlchemy does not create a table for BaseModel

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def save(self):
        """Update the updated_at timestamp whenever the object is modified"""
        self.updated_at = datetime.now()

    def update(self, data):
        """Update the attributes of the object based on the provided dictionary"""
        for key, value in data.items():
            if key == 'id' or key == 'created_at' or key == 'updated_at':
                continue  # (Skip read-only fields)
            if hasattr(self, key):
                setattr(self, key, value)
        self.save() 