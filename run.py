# run.py

from app import create_app
from app.extensions import db

app = create_app('config.DevelopmentConfig')

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)