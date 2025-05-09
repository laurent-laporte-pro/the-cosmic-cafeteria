"""
This module contains the database models for the Cosmic Cafeteria application.

The model is based on SQLAlchemy.
"""
from datetime import datetime
from enum import Enum

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, DateTime, Enum as SQLAEnum, Float, ForeignKey, Integer, String, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

db = SQLAlchemy()



class OrderStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class Hero(db.Model):
    __tablename__ = "heroes"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    planet = Column(String, nullable=False)
    

    orders = relationship("Order", back_populates="hero")
    allergies = relationship("Allergy", secondary="hero_allergies")

    def __repr__(self) -> str:
        return f"<Hero(id={self.id}, name='{self.name}', planet='{self.planet}')>"


class Allergy(db.Model):
    __tablename__ = "allergies"
    
    name = Column(String, primary_key=True)
    
    def __repr__(self) -> str:
        return f"<Allergy(name='{self.name}')>"

# Table association
hero_allergies = Table(
    "hero_allergies",
    db.Model.metadata,
    Column("hero_id", Integer, ForeignKey("heroes.id")),
    Column("allergy", String, ForeignKey("allergies.name")),
)

class Meal(db.Model):
    __tablename__ = "meals"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    origin_planet = Column(String, nullable=False)
    description = Column(String)

    ordered_by = relationship("Order", back_populates="meal")
    ingredients = relationship("Ingredient", secondary="meal_ingredients")

    def __repr__(self) -> str:
        return f"<Meal(id={self.id}, name='{self.name}', origin_planet='{self.origin_planet}')>"


class Ingredient(db.Model):
    __tablename__ = "ingredients"
    
    name = Column(String, primary_key=True)
    
    def __repr__(self) -> str:
        return f"<Ingredient(name='{self.name}')>"


# Association table
meal_ingredients = Table(
    "meal_ingredients",
    db.Model.metadata,
    Column("meal_id", Integer, ForeignKey("meals.id")),
    Column("ingredient", String, ForeignKey("ingredients.name")),
)


class Order(db.Model):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True)
    status = Column(SQLAEnum(OrderStatus), default=OrderStatus.PENDING, nullable=False)
    message = Column(String)
    order_time = Column(DateTime, default=datetime.utcnow, nullable=False)
    completed_time = Column(DateTime)
    
    # Foreign keys
    hero_id = Column(Integer, ForeignKey("heroes.id"), nullable=False)
    meal_id = Column(Integer, ForeignKey("meals.id"), nullable=False)
    
    # Relationships
    hero = relationship("Hero", back_populates="orders")
    meal = relationship("Meal", back_populates="ordered_by")

    def __repr__(self) -> str:
        return f"<Order(id={self.id}, status='{self.status}', hero_id={self.hero_id}, meal_id={self.meal_id})>"


# Import models to make them available when importing from the package
__all__ = ["db", "Hero", "Meal", "Order", "OrderStatus", "Ingredient", "Allergy"]
