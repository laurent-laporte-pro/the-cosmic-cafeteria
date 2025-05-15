from api.app_extensions import db
from typing import List, Optional


class Meal(db.Model):
    __tablename__ = "meals" 


    id: int = db.Column(db.Integer, primary_key=True)
    name: str = db.Column(db.String(100), nullable=False)
    ingredients = db.Column(db.JSON, nullable=False, default=list)
    price: float = db.Column(db.Float, nullable=False)
    origin_planet: str = db.Column(db.String(100), nullable=False)
    description: Optional[str] = db.Column(db.String(500), nullable=True)

    ordered_by = db.relationship('Order', backref='meal',
        passive_deletes=True,
        cascade="all, delete-orphan", 
        lazy=True
    )

    def __init__(
        self,
        name: str,
        ingredients: list[str],
        price: float,
        origin_planet: str,
        description: Optional[str] = None,
    ) -> None:
        self.name = name
        self.ingredients = ingredients
        self.price = price
        self.origin_planet = origin_planet
        self.description = description

    def __repr__(self) -> str:
        return f"<Meal id={self.id}, name={self.name}, origin_planet={self.origin_planet}>"

 