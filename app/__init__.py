from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_jwt_extended import JWTManager

# Start Flask app
app = Flask(__name__)
app.config.from_object('configuration.DevelopmentConfig')

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Initialize LoginManager
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

from app.models .user import User
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# import blueprints
from app.blueprints.gui import gui
app.register_blueprint(gui)
from app.blueprints.auth import auth
app.register_blueprint(auth)

# Import JWT
jwt = JWTManager(app)

# import API
from app.api.api import api, Users, Games, Token, Login
api.prefix = app.config["BASE_API_URL"]
api.add_resource(Users, "/users", "/users/<int:id>")
api.add_resource(Games, "/games", "/games/<int:id>")
api.add_resource(Token, "/token")
api.add_resource(Login, '/login')
api.init_app(app)

# Build DB
db.create_all()