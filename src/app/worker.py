import os

import redis
import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from api.models.order_worker import Order, Base
from datetime import datetime

# Setup Redis
#redis_client = redis.Redis(host='localhost', port=6379, db=0)
redis_client = redis.Redis.from_url(os.getenv("REDIS_URL"))

# Setup Database
#engine = create_engine('postgresql://user:password@localhost:5832/cosmic_cafeteria')  # or PostgreSQL, etc.
engine = create_engine(os.getenv("DATABASE_URL"))  # or PostgreSQL, etc.
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

print("Worker started. Waiting for orders...")

while True:
    _, data = redis_client.blpop('order_queue')
    order_json = json.loads(data)
    order = Order(
        customer_name=order_json['customer_name'],
        item=order_json['item'],
        created_at=datetime.fromisoformat(order_json['created_at'])
    )
    session.add(order)
    session.commit()
    print(f"Inserted Order: {order.customer_name} - {order.item}")

