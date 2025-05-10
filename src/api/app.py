from flask import Flask
from api.config import Config
from api.extensions import db, ma , redis_conn , task_queue , init_redis
from flask_migrate import Migrate

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize extensions
    db.init_app(app)
    ma.init_app(app)
    migrate = Migrate(app, db)
    
    with app.app_context():
        init_redis(app)

        from api.routes import hero_blueprint,meal_blueprint,order_blueprint  
        app.register_blueprint(hero_blueprint)
        app.register_blueprint(meal_blueprint)
        app.register_blueprint(order_blueprint)
        
        from api import models  # This ensures models are loaded
    return app

app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)