import pytest
from sqlalchemy.orm import Session
from api.models.order import Order, OrderStatus
from api.models.hero import Hero
from api.models.meal import Meal
from api.services.order_service import process_order_logic


@pytest.fixture
def setup_data(session: Session):
    # Create a hero with allergies
    hero = Hero(name="Thor", planet="Asgard", allergies=["Dust", "Iron"])
    session.add(hero)
    session.flush()  # Flush to assign id

    # Create a meal with ingredients that conflict with hero allergies
    meal_allergic = Meal(
        name="Dusty Meal",
        ingredients=["Dust", "Water"],
        price=10.0,
        origin_planet="Earth",
        description="A dusty meal"
    )
    session.add(meal_allergic)
    session.flush()

    # Create a meal with no conflicting ingredients
    meal_safe = Meal(
        name="Safe Meal",
        ingredients=["Water", "Salt"],
        price=15.0,
        origin_planet="Earth",
        description="A safe meal"
    )
    session.add(meal_safe)
    session.flush()

    # Create orders
    order_conflict = Order(hero_id=hero.id, meal_id=meal_allergic.id)
    order_safe = Order(hero_id=hero.id, meal_id=meal_safe.id)

    session.add_all([order_conflict, order_safe])
    session.commit()

    return {
        "hero": hero,
        "meal_allergic": meal_allergic,
        "meal_safe": meal_safe,
        "order_conflict": order_conflict,
        "order_safe": order_safe,
    }


def test_process_order_conflict(session: Session, setup_data):
    order = setup_data["order_conflict"]
    status = process_order_logic(session, order.id)
    assert status == OrderStatus.FAILED.name

    updated_order = session.get(Order, order.id)
    assert "allergic" in updated_order.message.lower()
    assert updated_order.status == OrderStatus.FAILED


def test_process_order_safe(session: Session, setup_data):
    order = setup_data["order_safe"]
    status = process_order_logic(session, order.id)
    assert status == OrderStatus.COMPLETED.name

    updated_order = session.get(Order, order.id)
    assert updated_order.message == "Success"
    assert updated_order.status == OrderStatus.COMPLETED
