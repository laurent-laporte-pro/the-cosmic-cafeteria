from sqlalchemy.orm import Session
from sqlalchemy import select

from api.models import Order, Hero, Meal, OrderStatus


def process_order_logic(db: Session, order_id: int) -> str:
    print('-----------------**before*******------------')
    order = db.get(Order, order_id)
    print('-----------------*********------------')
    if not order:
        raise ValueError("Order not found")

    hero = db.get(Hero, order.hero_id)
    meal = db.get(Meal, order.meal_id)

    
    if not hero or not meal:
        order.status = OrderStatus.CANCELLED
        order.message = "Hero or Meal not found"
    else:
        allergens = set(hero.allergies).intersection(set(meal.ingredients))
        if allergens:
            order.status = OrderStatus.CANCELLED
            order.message = f"Hero allergic to: {', '.join(allergens)}"
        else:
            order.status = OrderStatus.COMPLETED
            order.message = "Success"

    db.commit()
    return order.status.name
