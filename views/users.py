from flask import request
from flask_restx import Namespace, Resource

from dao.model.user import UserSchema
from helpers.decorators import super_user_required
from implemented import user_service

user_ns = Namespace("users")


@user_ns.route('/')
class UsersView(Resource):
    @super_user_required
    def get(self):
        users = user_service.get_all()

        return UserSchema(many=True).dump(users), 200

    def post(self):
        data = request.json

        user = user_service.create(data)

        return "", 201, {"location": f"/users/{user.id}"}


@user_ns.route('/<int:uid>')
class UserView(Resource):
    @super_user_required
    def get(self, uid):
        user = user_service.get_one(uid)
        one = UserSchema().dump(user)

        return one, 200

    @super_user_required
    def put(self, uid):
        req_json = request.json
        if "id" not in req_json:
            req_json["id"] = uid

        user_service.update(req_json)
        
        return "", 204

    @super_user_required
    def delete(self, uid):
        user_service.delete(uid)

        return "", 204

