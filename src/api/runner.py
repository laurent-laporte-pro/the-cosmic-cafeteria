from redis import Redis
from rq import Worker, Connection
from config.settings import settings

redis_conn = Redis.from_url(settings.REDIS_URL)

with Connection(redis_conn):
    # manage our worker
    worker = Worker(["default"])
    worker.work()