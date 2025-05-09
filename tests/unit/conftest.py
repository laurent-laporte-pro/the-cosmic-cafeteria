"""
Test fixtures specific to unit tests for the Cosmic Cafeteria API.
"""
import pytest
from unittest.mock import MagicMock, patch

from src.api.models import Hero, Meal, Order, Ingredient, Allergy


@pytest.fixture
def mock_hero():
    """Create a mock Hero object."""
    hero = MagicMock(spec=Hero)
    hero.id = 1
    hero.name = "Test Hero"
    hero.planet = "Test Planet"
    hero.allergies = []
    hero.orders = []
    return hero


@pytest.fixture
def mock_meal():
    """Create a mock Meal object."""
    meal = MagicMock(spec=Meal)
    meal.id = 1
    meal.name = "Test Meal"
    meal.description = "Test Description"
    meal.price = 9.99
    meal.vegan = True
    meal.origin_planet = "Test Planet"
    meal.ingredients = []
    return meal


@pytest.fixture
def mock_order():
    """Create a mock Order object."""
    order = MagicMock(spec=Order)
    order.id = 1
    order.hero_id = 1
    order.meal_id = 1
    order.quantity = 2
    order.status = "PENDING"
    order.message = None
    return order


@pytest.fixture
def mock_ingredient():
    """Create a mock Ingredient object."""
    ingredient = MagicMock(spec=Ingredient)
    ingredient.id = 1
    ingredient.name = "Test Ingredient"
    return ingredient


@pytest.fixture
def mock_allergy():
    """Create a mock Allergy object."""
    allergy = MagicMock(spec=Allergy)
    allergy.id = 1
    allergy.name = "Test Allergy"
    return allergy


@pytest.fixture
def mock_db_session():
    """Create a mock for the database session."""
    session = MagicMock()
    session.add.return_value = None
    session.commit.return_value = None
    session.delete.return_value = None
    session.query.return_value = session
    session.all.return_value = []
    return session