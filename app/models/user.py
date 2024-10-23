# user.py

from app.models.base_model import BaseModel
from email_validator import validate_email, EmailNotValidError

class User(BaseModel):
    def __init__(self, first_name, last_name, email, is_admin=False):
        super().__init__()
        try:
            valid = validate_email(email)
            self.email = valid.email
        except EmailNotValidError as e:
            raise ValueError(str(e))

        self.first_name = first_name
        self.last_name = last_name
        self.is_admin = is_admin
        self.places = []