"""
Worker tasks for The Cosmic Cafeteria.

This module contains tasks that are processed asynchronously by Redis Queue workers.
"""
import multiprocessing
import os
import random
import time
from datetime import datetime
import logging
from typing import Optional



logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


from ..api.models import db, Order, Hero, Meal, OrderStatus

def process_order(order_id: int) -> Optional[dict]:
    """Process an order asynchronously."""
    logger.info(f"Processing order {order_id}")
    

    from ..api import create_app
    
    app = create_app()
    
    with app.app_context():
        order = Order.query.get(order_id)
        
        if not order:
            logger.error(f"Order {order_id} not found")
            return None
        
        order.status = OrderStatus.IN_PROGRESS
        db.session.commit()
        logger.info(f"Order {order_id} status updated to IN_PROGRESS")
        
        
        processing_time = random.randint(1, 5)
        time.sleep(processing_time)
        
        
        hero = Hero.query.get(order.hero_id)
        meal = Meal.query.get(order.meal_id)
        
    
        hero_allergies = {allergy.name.lower() for allergy in hero.allergies}
        meal_ingredients = {ingredient.name.lower() for ingredient in meal.ingredients}
        
        # Alleries X Ingredients check
        allergic_ingredients = hero_allergies.intersection(meal_ingredients)
        
        if allergic_ingredients:
            order.status = OrderStatus.CANCELLED
            order.message = f"Order cancelled due to allergies: {', '.join(allergic_ingredients)}"
            order.completed_time = datetime.utcnow()
            db.session.commit()
            
            logger.info(f"Order {order_id} cancelled due to allergies: {allergic_ingredients}")
            return {
                "order_id": order_id,
                "status": "cancelled",
                "reason": f"Hero is allergic to: {', '.join(allergic_ingredients)}"
            }
        
        # if not allergies
        order.status = OrderStatus.COMPLETED
        order.completed_time = datetime.utcnow()
        db.session.commit()
        
        logger.info(f"Order {order_id} completed successfully")
        return {
            "order_id": order_id,
            "status": "completed",
            "processing_time": processing_time
        }