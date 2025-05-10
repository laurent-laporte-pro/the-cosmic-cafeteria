# src/api/extensions.py
from flask import current_app
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from redis import Redis
from rq import Queue

db = SQLAlchemy()
ma = Marshmallow()

# Initialize with None
redis_conn = None
task_queue = None

def init_redis(app):
    global redis_conn, task_queue
    redis_conn = Redis(
        host=app.config.get("REDIS_HOST", "tcc-redis"),
        port=app.config.get("REDIS_PORT", 6379),
        db=app.config.get("REDIS_DB", 0)
    )
    task_queue = Queue("task_queue", connection=redis_conn)
    app.extensions['redis'] = redis_conn
    app.extensions['task_queue'] = task_queue