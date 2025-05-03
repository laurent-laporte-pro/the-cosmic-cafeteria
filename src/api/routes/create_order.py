# app.py
import os

from flask_restful import Resource,reqparse
import redis
import json
from datetime import datetime

from api.models import order
from api.models.order import Orders

# Parser for POST data
order_parser = reqparse.RequestParser()
order_parser.add_argument('customer_name', type=str, required=True, help="Customer name is required")
order_parser.add_argument('item', type=str, required=True, help="Item is required")
#redis_client = redis.Redis(host='localhost', port=6379, db=0)
redis_client = redis.Redis.from_url(os.getenv("REDIS_URL"))


class OrderResource(Resource):
    def get(self):
        orders = Orders.query.all()
        return [{"id": order.id,'customer_name': order.customer_name,"item":order.item,
        "created_at":order.customer_name} for order in orders]
    def post(self):
        args = order_parser.parse_args()
        order_data = {
            'customer_name': args['customer_name'],
            'item': args['item'],
            'created_at': datetime.utcnow().isoformat()
        }
        redis_client.rpush('order_queue', json.dumps(order_data))
        return {'message': 'Order queued successfully'}, 201

