from importlib.resources import Resource
from urllib import request


from api.models.user import User
from cli.app import db, api

class UserResource(Resource):
    def get(self, user_id):
        user = User.query.get(user_id)
        if user:
            return user.json(), 200
        return {"message": "User not found"}, 404

    def put(self, user_id):
        data = request.get_json()
        user = User.query.get(user_id)
        if user:
            user.username = data.get('username', user.username)
            user.email = data.get('email', user.email)
            db.session.commit()
            return user.json(), 200
        return {"message": "User not found"}, 404

    def delete(self, user_id):
        user = User.query.get(user_id)
        if user:
            db.session.delete(user)
            db.session.commit()
            return {"message": "User deleted"}, 200
        return {"message": "User not found"}, 404

class UserListResource(Resource):
    def get(self):
        users = User.query.all()
        return [user.json() for user in users], 200

    def post(self):
        data = request.get_json()
        new_user = User(
            username=data['username'],
            email=data['email']
        )
        db.session.add(new_user)
        db.session.commit()
        return new_user.json(), 201

api.add_resource(UserListResource, '/users')
api.add_resource(UserResource, '/users/<int:user_id>')