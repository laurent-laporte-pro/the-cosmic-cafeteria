# tests/conftest.py

import pytest
from app import create_app
from api.app_extensions import db 
from api.models import Hero,Meal,Order,OrderStatus
from api.schemas import HeroSchema, MealSchema, OrderSchema


@pytest.fixture(scope="session")
def app():
    """
    app instance for testing.
    """
    app = create_app(env="testing")

    # Establish application context
    with app.app_context():
        yield app


@pytest.fixture
def session(app):
    with app.app_context():
        db.create_all()
        yield db.session
        db.session.rollback()
        db.drop_all()


### fixtures 

@pytest.fixture
def hero(session):
    test_hero = Hero(name="Thor", planet="Asgard", allergies=["Iron"])
    session.add(test_hero)
    session.commit()
    return test_hero

@pytest.fixture
def meal(session):
    test_meal = Meal(
        name="Starburger",
        ingredients=["Beef", "Starsauce"],
        price=12.99,
        origin_planet="Mars",
        description="interplanetary burger"
    )
    session.add(test_meal)
    session.commit()
    return test_meal


@pytest.fixture
def order(session, hero, meal):
    test_order = Order(
        hero_id=hero.id,
        meal_id=meal.id,
        status=OrderStatus.PENDING,
        message="deliver"
    )
    session.add(test_order)
    session.commit()
    return test_order


@pytest.fixture
def hero_schema():
    return HeroSchema()


@pytest.fixture
def meal_schema():
    return MealSchema()


@pytest.fixture
def order_schema():
    return OrderSchema()