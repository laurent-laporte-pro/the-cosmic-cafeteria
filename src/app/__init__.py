import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api

db = SQLAlchemy()

def create_app():
    template_dir = os.path.join(os.path.dirname(__file__), '../api/templates')
    app = Flask(__name__,template_folder=template_dir)
    app.config.from_object("app.config.Config")

    db.init_app(app)
    api = Api(app)
    api.init_app(app)

    # Import and register CLI
    from cli.commands import register_cli
    register_cli(app)

    # Register routes
    from api.routes.user_routes import UserResource
    from api.routes.create_order import OrderResource

    api.add_resource(UserResource, "/users")
    api.add_resource(OrderResource, "/order")

    # Register Jinja2 web routes
    from api.routes.user_pages import user_pages
    app.register_blueprint(user_pages)

    return app
