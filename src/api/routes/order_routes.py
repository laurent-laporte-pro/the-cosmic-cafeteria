"""
Order routes for the Cosmic Cafeteria API.

This module implements endpoints for managing orders, including creating, listing, and processing orders.
"""
from datetime import datetime

from flask import current_app
from flask_restful import Resource, marshal_with, reqparse, fields
import redis
from rq import Queue

from ..models import Hero, Meal, Order, OrderStatus, db
from ..schemas import order_schema


class OrderResource(Resource):
    
    @marshal_with(order_schema)
    def get(self, order_id):
        """Get an order by id."""
        order = Order.query.get_or_404(order_id)
        return order, 200
    
    @marshal_with(order_schema)
    def post(self):
        """Create a new order and queue it for processing."""
        parser = reqparse.RequestParser()
        parser.add_argument(
            'hero_id', 
            type=int, 
            required=True, 
            help='Hero_id is required',
            location=['form', 'json']
        )
        parser.add_argument(
            'meal_id', 
            type=int, 
            required=True, 
            help='Meal_D is required',
            location=['form', 'json']
        )
        args = parser.parse_args()

        # hero and meal exist?
        hero = Hero.query.get(args['hero_id'])
        if not hero:
            return {'message': f"Hero with ID {args['hero_id']} not found"}, 404
        
        meal = Meal.query.get(args['meal_id'])
        if not meal:
            return {'message': f"Meal with ID {args['meal_id']} not found"}, 404
        
        # Create order with PENDING status
        order = Order(
            hero_id=args['hero_id'],
            meal_id=args['meal_id'],
            status=OrderStatus.PENDING,
            order_time=datetime.utcnow()
        )
        
        db.session.add(order)
        db.session.commit()
        
        # Send task to Redis queue
        try:
            redis_url = current_app.config.get('REDIS_URL', 'redis://tcc-redis:6379/0')
            redis_conn = redis.from_url(redis_url)
            
            # Create queue
            queue = Queue('order_processing', connection=redis_conn)
            
            # Enqueue the task
            queue.enqueue('src.worker.tasks.process_order', order.id, job_timeout=300)
            
            return order, 202
        
        except Exception as e:
            current_app.logger.error(f"Failed to enqueue order {order.id}: {str(e)}")
            return {
                'id': order.id,
                'status': order.status.value,
                'message': 'Order created but processing delayed',
                'error': str(e)
            }, 202

    def delete(self, order_id):
        """Delete an order or mark it as cancelled."""
        order = Order.query.get_or_404(order_id)
        
        parser = reqparse.RequestParser()
        parser.add_argument(
            'message',
            type=str,
            required=True,
            help='Message is required when cancelling an order',
            location=['form', 'json'],
            trim=True
        )
        
        args = parser.parse_args()
        
        if order.status in [OrderStatus.PENDING, OrderStatus.IN_PROGRESS]:
            order.status = OrderStatus.CANCELLED
            order.message = args['message']
            order.completed_time = datetime.utcnow()
            
            db.session.commit()
            
            return {'message': f"Order {order_id} cancelled: {args['message']}"}, 200
        else:
            db.session.delete(order)
            db.session.commit()
            return '', 204