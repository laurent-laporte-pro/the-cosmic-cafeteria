from redis import Redis
from rq import Queue
from config.settings import settings

redis_conn = Redis.from_url(settings.REDIS_URL)
default_queue = Queue("default", connection=redis_conn)

# if you later want to add multiple queues for different job priorities high,low....