from flask import Flask, jsonify

from config import get_config
from api.app_extensions import db


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

    # Register core routes like health checks and error handlers
    _register_internal_routes(app)

    return app


def _init_extensions(app: Flask) -> None:
    """
    Initialize Flask extensions 'SQLAlchemy' 
    """
    db.init_app(app)
  


def _register_internal_routes(app: Flask) -> None:
    """
    Define internal endpoints in our case we need health check func
    """

    @app.route("/health", methods=["GET"])
    def health_check():
        return jsonify(status="ok", environment=app.config.get("ENV")), 200

