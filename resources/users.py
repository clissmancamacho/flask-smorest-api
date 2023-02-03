import os
from flask import redirect, request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from passlib.hash import pbkdf2_sha256 as sha256
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, get_jwt, jwt_required
from urllib.parse import urlencode

from blocklist import BLOCKLIST
from db import db
from models import UserModel
from schemas import UserSchema
from utils import oauth2_claveunica

blp = Blueprint("Users", __name__, description="Operations on users")


@blp.route("/oauth")
class UserOAuth(MethodView):
    def get(self):
        auth_request_data = {
            'client_id': os.getenv('CLAVE_UNICA_CLIENT_ID'),
            'redirect_uri': os.getenv('CLAVE_UNICA_REDIRECT_URI'),
            # 'state': oauth2_claveunica.generate_state(),
            'state': 'asdasdas',
            'response_type': 'code',
            'scope': 'openid run name email',
            'prompt': 'login'
        }

        auth_url_endpoint = os.getenv('CLAVEUNICA_AUTH_ENDPOINT')
        query_string = urlencode(auth_request_data)
        url = f'{auth_url_endpoint}?{query_string}'

        return redirect(url)


@blp.route("/callback/claveunica")
class UserOAuthCallback(MethodView):
    def get(self):
        authorization_code = request.args.get('code')
        state = request.args.get('state')

        access_token_json = oauth2_claveunica.request_authorization_code(
            'https://accounts.claveunica.gob.cl/openid/token',
            os.getenv('CLAVE_UNICA_CLIENT_ID'),
            os.getenv('CLAVE_UNICA_CLIENT_SECRET'),
            os.getenv('CLAVE_UNICA_REDIRECT_URI'),
            authorization_code,
            state
        )
        access_token = access_token_json.get('access_token')
        # obtener info usuario
        info_user_json = oauth2_claveunica.request_info_user(
            'https://accounts.claveunica.gob.cl/openid/userinfo',
            access_token
        )
        return info_user_json


@blp.route("/register")
class UserRegister(MethodView):
    @blp.arguments(UserSchema)
    @blp.response(201)
    def post(self, user_data):
        if UserModel.query.filter(UserModel.username == user_data["username"]).first():
            abort(409, message="A user with that username already exists.")
        user = UserModel(
            username=user_data["username"], password=sha256.hash((user_data["password"])))
        db.session.add(user)
        db.session.commit()

        return {"message": "User created successfully."}, 201


@blp.route("/login")
class UserLogin(MethodView):
    @blp.arguments(UserSchema)
    def post(self, user_data):
        user = UserModel.query.filter(
            UserModel.username == user_data["username"]).first()
        if user and sha256.verify(user_data["password"], user.password):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(identity=user.id)
            return {"access_token": access_token, "refresh_token": refresh_token}, 200

        abort(401, message="Invalid credentials.")


@blp.route("/refresh")
class TokenRefresh(MethodView):
    @jwt_required(refresh=True)
    def get(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        # Only Allow generate one refresh token per user
        # jti = get_jwt()["jti"]
        # BLOCKLIST.add(jti)
        return {"access_token": new_token}, 200


@blp.route("/user/<int:user_id>")
class User(MethodView):
    @blp.response(200, UserSchema)
    def get(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        return user

    def delete(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return {"message": "User deleted."}, 200


@blp.route("/logout")
class UserLogout(MethodView):
    @jwt_required()
    def get(self):
        jti = get_jwt()["jti"]
        BLOCKLIST.add(jti)
        return {"message": "Successfully logged out."}, 200
