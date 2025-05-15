from flask import Flask, jsonify

from config import get_config
from api.app_extensions import db
from api.routes.hero_route import hero_bp
from api.routes.meal_route import meal_bp
from api.routes.order_route import order_bp
from flasgger import Swagger


def create_app(env: str | None = None) -> Flask:
    """
    Application factory for creating a Flask app instance with all
    configuration, extensions
    """
    # Load config based on environment
    config = get_config(env)

    # Initialize Flask app
    app = Flask(__name__)
    app.config.from_object(config)

    # Initialize core extensions
    _init_extensions(app)

    # Register blueprints
    register_blueprints(app)

    # enable logging 
    config.init_log_app(app)

    # Register core routes like health checks and error handlers
    _register_internal_routes(app)

    add_swager(app)

    return app


def _init_extensions(app: Flask) -> None:
    """
    Initialize Flask extensions 'SQLAlchemy' 
    """
    db.init_app(app)

def add_swager(app: Flask) -> None: 


    swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": 'apispec_1',
            "route": '/apispec_1.json',
            "rule_filter": lambda rule: True,
            "model_filter": lambda tag: True,
        }
    ],
        "static_url_path": "/flasgger_static",
        "swagger_ui": True,
        "specs_route": "/apidocs/"
    }

    swagger_template = {
        "swagger": "2.0",
        "info": {
            "title": "My Flask API",
            "description": "API for adding two numbers",
            "version": "1.0.0"
        },
    }
    swagger = Swagger(app, config=swagger_config, template=swagger_template)
  


def _register_internal_routes(app: Flask) -> None:
    """
    Define internal endpoints in our case we need health check func
    """

    @app.route("/health", methods=["GET"])
    def health_check():
        return jsonify(status="ok", environment=app.config.get("ENV")), 200


def register_blueprints(app: Flask) -> None:
    app.register_blueprint(hero_bp, url_prefix="/api")
    app.register_blueprint(meal_bp, url_prefix="/api")
    app.register_blueprint(order_bp, url_prefix="/api")
