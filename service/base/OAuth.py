import os
from flask_restx import Namespace, Resource
from flask import request, redirect, make_response
from pathlib import PurePath
import requests
from .database import db
import jwt
from ..config import JWT_KEY, JWT_ALGORITHM

KAKAO_CLIENT_ID = os.environ.get('KAKAO_CLIENT_ID')

auth = Namespace('auth', description='Social login APIs')

@auth.route('/kakao')
class KakaoSignIn(Resource):
    def get(self):
        ppath = PurePath(request.url_root)
        redirect_url = str(ppath.parent.joinpath('kakao_signin'))
        kakao_oauth_url = f"https://kauth.kakao.com/oauth/authorize?client_id={KAKAO_CLIENT_ID}&redirect_url={redirect_url}&response_type=code"
        return redirect(kakao_oauth_url)


@auth.route('/kakao/callback')
class KakaoSignIn(Resource):
    def get(self):
        try:
            code = request.args.get['code']
            redirect_uri = request.url_root
            token_request = requests.get(f"https://kauth.kakao.com/oauth/token?grant_type=authorization_code&client_id={KAKAO_CLIENT_ID}&redirect_uri={redirect_uri}&code={code}")
            token_json = token_request.json()
            error = token_json.get('error', None)
            if error is not None:
                return make_response({'message': 'INVALID_CODE'}, 400)
            access_token = token_json.get('access_token')

            profile_request = requests.get("https://kapi.kakao.com/v2/user/me", headers={"Authorization" : f"Bearer {access_token}"})
            data = profile_request.json()
        except KeyError:
            return make_response({"message": "INVALID_TOKEN"}, 400)
        except access_token.DoesNotExists:
            return make_response({"message": "INVALID_TOKEN"}, 400)
        return kakao_sign(data)


def kakao_sign(data):
    kakao_account = data.get('properties')
    email = kakao_account.get('nickname', None)
    kakao_id = str(data.get('id'))

    users = db.users
    user = users.find_one({'email': email})
    if not user:
        new_user = {
            'email': email,
            'kakao_id': kakao_id,
            'privilege': None
        }
        id = users.insert_one(new_user).inserted_id
        token = jwt.encode({'id': str(id)}, JWT_KEY, JWT_ALGORITHM)
        token = token.decode('utf-8')

        return {
            'status': 'success',
            'message': 'you become a member for our service',
            'Authorization': token
        }, 200
    else:
        id = str(user._id)
        token = jwt.encode({'id': str(id)}, JWT_KEY, JWT_ALGORITHM)
        token = token.decode('utf-8')

        return {
            'status': 'already signin',
            'message': 'you already our member. login success',
            'Authorization': token
        }, 201