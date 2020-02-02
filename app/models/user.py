from flask_login import UserMixin
from app import db,app
from sqlalchemy.orm import relationship
from werkzeug.security import check_password_hash

class User(UserMixin, db.Model):

    __tablename__ = 'tUser'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(100))
    games = relationship("Game")

    def verify_password(self,password):
        return check_password_hash(self.password, password)
