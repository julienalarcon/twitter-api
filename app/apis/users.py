# pylint: disable=missing-docstring

from flask import request
from flask_restx import Namespace, Resource, fields
from app.models import User
from app import db

api = Namespace("users")
model = api.model(
    "User",
    {
        "id": fields.Integer,
        "username": fields.String,
        "email": fields.String,
        "api_key": fields.String,
    },
)

create_user_fields = api.model(
    "CreateUserModel",
    {
        "username": fields.String(description="Username", required=True),
        "email": fields.String(description="User's Email", required=True),
    },
)

update_user_fields = api.model(
    "CreateUserModel",
    {
        "username": fields.String(description="Username"),
        "email": fields.String(description="User's Email"),
    },
)


@api.route("")
class UserMain(Resource):
    @api.doc(responses={400: "Invalid payload", 200: "User Created"})
    @api.marshal_with(model, code=200)
    @api.expect(create_user_fields, validate=True)
    def post(self):
        payload = request.json
        user = User(
            username=payload["username"],
            email=payload["email"],
            api_key=(payload["api_key"] if "api_key" in payload else ""),
        )
        db.session.add(user)
        db.session.commit()
        return user, 200

    @api.doc(responses={200: "Success"})
    @api.marshal_with(model, as_list=True, code=200)
    def get(self):
        return db.session.query(User).all(), 200


@api.route("/<int:user_id>", endpoint="user-by-id")
@api.doc(responses={404: "User not found"})
@api.param("user_id", "The user unique identifier")
class UserById(Resource):
    @api.marshal_with(model, code=200)
    @api.doc(responses={200: "User Found"})
    def get(self, user_id):
        user = db.session.query(User).get(user_id)
        if user is None:
            api.abort(404)
        else:
            return user, 200

    @api.marshal_with(model, code=200)
    @api.doc(responses={400: "Invalid payload", 200: "User Updated"})
    @api.expect(update_user_fields, validate=True)
    def patch(self, user_id):
        payload = request.json
        user = db.session.query(User).get(user_id)

        if user is None:
            api.abort(404)

        user.username = payload["username"] if "username" in payload else user.username
        user.email = payload["email"] if "email" in payload else user.email
        db.session.commit()

        return user, 200

    @api.doc(responses={204: "User Deleted"})
    def delete(self, user_id):
        user = db.session.query(User).get(user_id)

        if user is None:
            api.abort(404)

        db.session.delete(user)
        db.session.commit()
        return "", 204
