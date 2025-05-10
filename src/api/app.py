from flask import Flask
from api.config import Config
from api.extensions import db, ma
from flask_migrate import Migrate

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize extensions
    db.init_app(app)
    ma.init_app(app)
    migrate = Migrate(app, db)
    
    # Import and register blueprints within app context
    with app.app_context():
        from api.routes import hero_blueprint,meal_blueprint,order_blueprint  # Adjust import path
        app.register_blueprint(hero_blueprint)
        app.register_blueprint(meal_blueprint)
        app.register_blueprint(order_blueprint)
        
        # Import models to ensure they're registered with SQLAlchemy
        from api import models  # This ensures models are loaded
        
    return app

app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)