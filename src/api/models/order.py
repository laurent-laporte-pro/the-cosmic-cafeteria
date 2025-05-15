from datetime import datetime
from typing import Optional
from api.app_extensions import db
import enum


class OrderStatus(enum.Enum):
    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"


class Order(db.Model):
    __tablename__ = "orders"

    id: int = db.Column(db.Integer, primary_key=True)
    status: OrderStatus = db.Column(
        db.Enum(OrderStatus), nullable=False, default=OrderStatus.PENDING
    )
    message: Optional[str] = db.Column(db.String(500), nullable=True)
    order_time: datetime = db.Column(db.DateTime, default=datetime.utcnow)
    completed_time: Optional[datetime] = db.Column(db.DateTime, nullable=True)
    hero_id: int = db.Column(db.Integer, db.ForeignKey("heroes.id", ondelete='cascade'), nullable=False)
    meal_id: int = db.Column(db.Integer, db.ForeignKey("meals.id", ondelete='cascade'), nullable=False)

    def __init__(
        self,
        hero_id: int,
        meal_id: int,
        status: OrderStatus = OrderStatus.PENDING,
        message: Optional[str] = None,
    ) -> None:
        self.hero_id = hero_id
        self.meal_id = meal_id
        self.status = status
        self.message = message

    def __repr__(self) -> str:
        return (
            f"<Order id={self.id}, hero_id={self.hero_id}, "
            f"meal_id={self.meal_id}, status={self.status.name}, "
            f"order_time={self.order_time}>"
        )

   