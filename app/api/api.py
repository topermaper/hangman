from flask_restful import Api, Resource
from flask import request, jsonify, g, url_for, abort, make_response
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash

from app import app, db, api
from app.models.user import User
from app.models.hangman import Hangman

auth = HTTPBasicAuth()
api = Api()

@auth.verify_password
def verify_password(email_or_token, password):

    if email_or_token == None:
        return False

    # first try to authenticate by token
    user = User.verify_auth_token(email_or_token)

    if not user:
        # authenticate with email and password
        user = User.query.filter_by(email = email_or_token).first()

        if not user or not user.verify_password(password):
            return False

    g.user = user
    return True


class Users(Resource):

    @auth.login_required
    def get(self, id):

        # We don't have permission to retrieve this user
        if g.user.id != id:
            abort(401)

        user = User.query.get_or_404(id)

        return jsonify({ "email":user.email, "name": user.name })

    def post(self):
        name     = request.json.get("name")
        email    = request.json.get("email")
        password = request.json.get("password")

        # missing arguments
        if name is None or email is None or password is None:
            abort(400)
        # this user does not exist
        if User.query.filter_by(email = email).first() is not None:
            abort(400)

        # create new user hashing the password
        new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'))

        db.session.add(new_user)
        db.session.commit()

        # Return resource location in the response header
        res = make_response(jsonify({ 'email' : new_user.email, 'name':  new_user.name  }), 201)
        res.headers["Location"] = api.url_for(self, id = new_user.id, _external = True)
        return res


class Games(Resource):

    @auth.login_required
    def get(self, id):
        game = Hangman.query.get_or_404(id)

        # We don't have permission to retrieve this game
        if g.user.id != game.user_id:
            abort(401)

        return jsonify({ "id":game.id, "secret_word": game.secret_word, "score" : game.score, "multiplier" :game.multiplier, "user_guess" : game.get_user_guess(), "misses" : game.misses, "status":game.status})

    @auth.login_required
    def post(self):

        game = Hangman(g.user.id)

        db.session.add(game)
        db.session.commit()

        # Return resource location in the response header
        res = make_response('', 201)
        res.headers["Location"] = api.url_for(self, id = game.id, _external = True)
        return res

    @auth.login_required
    def patch(self, id):
        user_guess = request.json.get("user_guess")

        # missing arguments
        if user_guess is None:
            abort(400)

        game = Hangman.query.get_or_404(id)

        # We don't have permission to patch this game
        if g.user.id != game.user_id:
            abort(401)

        if game.status != 'ACTIVE':
            abort(422)

        # The user guess is not accepted
        if not game.set_user_guess(user_guess):
            abort(422)

        db.session.add(game)
        db.session.commit()

        # Resource Patched
        res = make_response(jsonify({ 'message' : 'Game was updated' }), 204)
        return res

class Token(Resource):
    @auth.login_required
    def get(self):
        token = g.user.generate_auth_token()
        return jsonify({"token": token.decode("ascii"), "duration": app.config['TOKEN_EXPIRATION'] })