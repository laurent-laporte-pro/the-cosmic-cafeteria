from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object("app.config.Config")

    db.init_app(app)
    api = Api(app)
    api.init_app(app)

    # Import and register CLI
    from cli.commands import register_cli
    register_cli(app)

    # Register routes
    from api.routes.user_routes import UserResource
    from api.models.user import User

    api.add_resource(UserResource, "/users")

    return app
