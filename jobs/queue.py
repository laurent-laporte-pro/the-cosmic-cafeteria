from redis import Redis
from rq import Queue
from config import Config

redis_conn = Redis.from_url(Config.REDIS_URL)
default_queue = Queue("default", connection=redis_conn)

# if you later want to add multiple queues for different job priorities high,low....