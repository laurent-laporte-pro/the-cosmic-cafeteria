import pytest
from datetime import datetime
from src.api.models import (
    Hero,
    Meal,
    Order,
    OrderStatus,
)

# --- Hero Model Tests ---
def test_hero_creation():
    """Test basic hero creation with allergies"""
    hero = Hero(name="Superman", allergies=["kryptonite", "magic"])
    assert hero.name == "Superman"
    assert hero.allergies == ["kryptonite", "magic"]
    assert isinstance(hero.allergies, list)


def test_hero_relationship_with_orders():
    """Test hero can have multiple orders"""
    hero = Hero(name="Wonder Woman")
    order1 = Order(status=OrderStatus.PENDING)
    order2 = Order(status=OrderStatus.COMPLETED)
    hero.orders.extend([order1, order2])
    
    assert len(hero.orders) == 2
    assert order1.hero == hero
    assert order2.hero == hero

# --- Meal Model Tests ---
def test_meal_creation():
    """Test meal creation with ingredients"""
    meal = Meal(name="Plutonian Pie", ingredients=["moon dust", "cosmic berries"])
    assert meal.name == "Plutonian Pie"
    assert meal.ingredients == ["moon dust", "cosmic berries"]
    assert isinstance(meal.ingredients, list)



def test_meal_relationship_with_orders():
    """Test meal can be ordered multiple times"""
    meal = Meal(name="Mars Salad")
    order1 = Order(status=OrderStatus.PENDING)
    order2 = Order(status=OrderStatus.COMPLETED)
    meal.orders.extend([order1, order2])
    
    assert len(meal.orders) == 2
    assert order1.meal == meal
    assert order2.meal == meal

# --- Order Model Tests ---
def test_order_creation():
    """Test basic order creation"""
    order = Order()
    assert order.status == OrderStatus.PENDING
    assert isinstance(order.created_at, datetime)
    assert order.processed_at is None


def test_order_invalid_status():
    """Test invalid status assignment"""
    order = Order()
    with pytest.raises(ValueError):
        order.status = "INVALID_STATUS"

def test_order_relationships():
    """Test order connects to hero and meal"""
    hero = Hero(name="Flash")
    meal = Meal(name="Lightning Soup")
    order = Order(hero=hero, meal=meal)
    
    assert order.hero == hero
    assert order.meal == meal
    assert order in hero.orders
    assert order in meal.orders


