from rq import Worker
from api.extensions import redis_conn

def create_worker():
    #checking if there is a redis connection
    if not redis_conn:
        raise ValueError("Redis connection is not initialized. Check app.py.")

    # Create and return the worker for the 'default' queue
    return Worker(queues=['default'], connection=redis_conn)
