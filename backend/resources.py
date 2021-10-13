from flask import request
from flask_restful import Resource, marshal_with, fields
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from exceptions import BadRequest, Unauthorized

import config
from services import user_service

class UserCRUD(Resource):

    @marshal_with(user_service.user_api_fields)
    def get(self):
        return user_service.get_all()

    @marshal_with(user_service.user_request_api_fields)
    def post(self):
        data = request.get_json()
        return user_service.create_user(**data)


class User(Resource):

    @marshal_with(user_service.user_api_fields)
    @jwt_required()
    def get(self):
        email, id = get_jwt_identity()
        return user_service.get_user(id)

class ForgetUser(Resource):

    @marshal_with(user_service.user_api_fields)
    def post(self, id):
        return user_service.forget_user(id)


class UserRequest(Resource):

    @marshal_with(user_service.user_request_api_fields)
    @jwt_required()
    def get(self):
        email, id = get_jwt_identity()
        user_service.check_is_operator(id)
        return user_service.get_unevaluated_user_requests()


class UserRequestDetail(Resource):

    @marshal_with(user_service.user_request_api_fields)
    def get(self, id):
        return user_service.get_user_request(id)

    @marshal_with(user_service.user_api_fields)
    @jwt_required()
    def put(self, request_id):
        data = request.get_json()
        action = data.get('action')
        email, id = get_jwt_identity()
        user_service.check_is_operator(id)
        if action == 'approve':
            return user_service.approve_request(id, request_id)
        else:
            return user_service.disapprove_request(id, request_id)


class Login(Resource):

    def post(self):
        email = request.json.get('email', None)
        password = request.json.get('password', None)

        if email is None or password is None:
            raise BadRequest("Missing username or password parameter")

        if not user_service.check_password(email, password):
            raise Unauthorized("Bad username or password")

        user = user_service.get_user_by_email(email)

        access_token = create_access_token(identity=(email, user.id))
        return {"message": "User authenticated successfully", "access_token" : access_token}


class Auth(Resource):

    @marshal_with(user_service.user_api_fields)
    @jwt_required()
    def get(self):
        email, id = get_jwt_identity()
        return user_service.get_user(id)


class Image(Resource):

    @marshal_with(user_service.user_api_fields)
    @jwt_required()
    def post(self):
        email, id = get_jwt_identity()
        data = request.get_json()
        image = data.get('image')
        return user_service.add_image(id, image, data)


class User(Resource):

    @marshal_with(user_service.user_api_fields)
    @jwt_required()
    def put(self):
        email, id = get_jwt_identity()
        data = request.get_json()
        return user_service.update_user(id, data)


class RequestResetPassword(Resource):

    def post(self):
        data = request.get_json()
        email = data.get('email')
        r = user_service.request_password_reset(email)
        if r is not None:
            return { "message": "User password reset request created successfully" }
        else:
            raise BadRequest()


class ResetPassword(Resource):

    def post(self):
        data = request.get_json()
        token = data.get('token')
        password = data.get('password')
        r = user_service.reset_password(token, password)
        if r is not None:
            return { "message": "User password has been reset successfully" }
        else:
            raise BadRequest()


class AddInteraction(Resource):

    @marshal_with(user_service.interaction_api_fields)
    @jwt_required()
    def post(self):
        data = request.get_json()
        email, id = get_jwt_identity()
        return user_service.add_interaction(id, data.get('id'), data)


class Info(Resource):

    def get(self):
        return { "environment": config.ENVIRONMENT }
