from flask_restful import Resource
from flask import request
from app import db
from api.models.user import User

class UserResource(Resource):
    def get(self):
        users = User.query.all()
        return [{"id": u.id, "username": u.username} for u in users]

    def post(self):
        data = request.json
        new_user = User(username=data["username"])
        db.session.add(new_user)
        db.session.commit()
        return {"message": "User created", "id": new_user.id}
