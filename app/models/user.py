from flask_login import UserMixin
from app import db,app
from sqlalchemy.orm import relationship
from itsdangerous import TimedJSONWebSignatureSerializer, BadSignature, SignatureExpired
from werkzeug.security import check_password_hash

class User(UserMixin, db.Model):

    __tablename__ = 'tUser'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(100))
    games = relationship("Game")


    def generate_auth_token(self):
        s = TimedJSONWebSignatureSerializer(app.config['SECRET_KEY'], expires_in = app.config['TOKEN_EXPIRATION'])
        return s.dumps({ 'id': self.id })

    def verify_password(self,password):
        return check_password_hash(self.password, password)

    @staticmethod
    def verify_auth_token(token):
        print("verify_auth_token token:{}".format(token))
        s = TimedJSONWebSignatureSerializer(app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except BadSignature:
            # Token is invalid
            return None 
        except SignatureExpired:
            # The token expired, valid though
            return None 

        return User.query.get(data['id'])