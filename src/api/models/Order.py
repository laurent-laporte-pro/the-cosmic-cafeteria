from datetime import datetime
from api.extensions import db
from api.models.order_status import OrderStatus

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.Enum(OrderStatus), nullable=False, default=OrderStatus.PENDING)
    message = db.Column(db.String(500), nullable=True)
    order_time = db.Column(db.DateTime, default=datetime.utcnow)
    completed_time = db.Column(db.DateTime, nullable=True)

    hero_id = db.Column(db.Integer, db.ForeignKey('hero.id'), nullable=False)
    meal_id = db.Column(db.Integer, db.ForeignKey('meal.id'), nullable=False)

    def __init__(self, hero, meal, status, message=None):
        self.hero = hero
        self.meal = meal
        self.status = status
        self.message = message

    def __repr__(self):
        return f'order #{id} : hero id {self.hero_id} ordered {self.meal_id} at {self.order_time}'