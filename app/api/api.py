from flask_restful import Api, Resource
from flask import request, jsonify, url_for, abort, make_response
from werkzeug.security import generate_password_hash
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt

from app import app, db, api
from app.models.user import User
from app.models.hangman import Hangman


api = Api()

class Login(Resource):
    def post(self):

        email    = request.json.get("email")
        password = request.json.get("password")

        # missing arguments
        if email is None or password is None:
            abort(400, "Email or password is missing")

        user = User.query.filter_by(email = email).first()
        # this user already exist
        if user is None:
            abort(400, "Non existent user '{}'".format(email))

        # Incorrect password
        if not user.verify_password(password):
            abort(400, "Wrong credentials")

        access_token  = create_access_token(identity = user.id)
        refresh_token = create_refresh_token(identity = user.id)

        res = make_response(jsonify({
            'access_token': access_token,
            'refresh_token': refresh_token,
            'message': 'Logged in as {}'.format(user.email),
            }), 200)

        # Return user resource in location header
        res.headers["Location"] = api.url_for(Users, id = user.id, _external = True)
        return res

class Users(Resource):

    @jwt_required
    def get(self, id=None):

        # Inexistent resource
        if id == None:
            abort(404)
        user = User.query.get_or_404(id)

        # Don't have permission to retrieve this user
        if get_jwt_identity() != id:
            abort(401)

        res = make_response(jsonify({
            "email":user.email,
            "name": user.name
            }), 200)

        res.headers["Location"] = api.url_for(self, id = user.id, _external = True)
        return res


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

        try:
            db.session.add(new_user)
            db.session.commit()
            access_token  = create_access_token(identity = id)
            refresh_token = create_refresh_token(identity = id)
        except:
            abort(500)

        # Return resource location in the response header
        res = make_response(jsonify({
            'access_token': access_token,
            'refresh_token': refresh_token,
            'email' : new_user.email,
            'name':  new_user.name
            }), 201)

        res.headers["Location"] = api.url_for(self, id = new_user.id, _external = True)

        return res


class Games(Resource):

    @jwt_required
    def get(self, id=None):

        # Inexistent resource
        if id == None:
            abort(404)
        game = Hangman.query.get_or_404(id)
        
        # We don't have permission to retrieve this game
        if get_jwt_identity() != game.user_id:
            abort(401)

        # Return resource location in the response header
        res = make_response(jsonify({
            "id":game.id,
            "secret_word": game.secret_word,
            "score" : game.score,
            "multiplier" :game.multiplier,
            "user_guess" : game.user_guess_list,
            "misses" : game.misses,
            "status":game.status
            }), 200)

        res.headers["Location"] = api.url_for(self, id = game.id, _external = True)

        return res

            
    @jwt_required
    def post(self):

        game = Hangman(get_jwt_identity())

        db.session.add(game)
        db.session.commit()

        # Return resource location in the response header
        res = make_response(jsonify({
            "id":game.id,
            "secret_word": game.secret_word,
            "score" : game.score,
            "multiplier" :game.multiplier,
            "user_guess" : game.user_guess_list,
            "misses" : game.misses,
            "status":game.status
            }), 201)

        res.headers["Location"] = api.url_for(self, id = game.id, _external = True)

        return res

    @jwt_required
    def patch(self, id=None):
        # Inexistent resource
        if id == None:
            abort(404)
        game = Hangman.query.get_or_404(id)

        user_guess = request.json.get("user_guess")

        # missing arguments
        if user_guess is None:
            abort(400,"Missing field 'user_guess'")

        # We don't have permission to patch this game
        if get_jwt_identity() != game.user_id:
            abort(401,"You can only play your own games")

        if game.status != 'ACTIVE':
            abort(422,'Game is finished')

        # The user guess is not accepted
        if not game.set_user_guess(user_guess):
            abort(422, "Invalid parameter 'user_guess'")

        db.session.add(game)
        db.session.commit()

        # Return patched resource
        # Return resource location in the response header
        res = make_response(jsonify({
            "id":game.id,
            "secret_word": game.secret_word,
            "score" : game.score,
            "multiplier" :game.multiplier,
            "user_guess" : game.user_guess_list,
            "misses" : game.misses,
            "status":game.status
            }), 200)

        res.headers["Location"] = api.url_for(self, id = game.id, _external = True)

        return res


class Token(Resource):
    @jwt_refresh_token_required
    def post(self):
        access_token = create_access_token(identity = get_jwt_identity())

        return  jsonify({'access_token': access_token},200)
