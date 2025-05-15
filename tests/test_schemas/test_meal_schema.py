import pytest
from marshmallow import ValidationError

def test_meal_schema_valid(meal_schema):
    data = {
        "name": "Meal",
        "ingredients": ["example1", "exampl2", "example3"],
        "price": 9.99,
        "origin_planet": "Earth",
        "description": "exampl desk."
    }
    meal = meal_schema.load(data)
    assert meal.name == "Meal"
    assert "exampl2" in meal.ingredients
    assert meal.price == 9.99
    assert meal.origin_planet == "Earth"
    assert meal.description == "exampl desk."

def test_meal_schema_missing_required(meal_schema):
    data = {
        "ingredients": ["Bun", "Patty"],
        "price": 5.0
        # missing 'name' and 'origin_planet'
    }
    with pytest.raises(ValidationError) as excinfo:
        meal_schema.load(data)
    errors = excinfo.value.messages
    assert "name" in errors
    assert "origin_planet" in errors

def test_meal_schema_empty_ingredients(meal_schema):
    data = {
        "name": "Empty Meal",
        "ingredients": [],
        "price": 5.0,
        "origin_planet": "Mars"
    }
    with pytest.raises(ValidationError) as excinfo:
        meal_schema.load(data)
    errors = excinfo.value.messages
    assert "ingredients" in errors

def test_meal_schema_invalid_price(meal_schema):
    data = {
        "name": "Meal",
        "ingredients": ["Igred"],
        "price": 0,  # invalid, must be > 0
        "origin_planet": "Venus"
    }
    with pytest.raises(ValidationError) as excinfo:
        meal_schema.load(data)
    errors = excinfo.value.messages
    assert "price" in errors

def test_meal_schema_description_optional(meal_schema):
    data = {
        "name": "Simple Meal",
        "ingredients": ["Water"],
        "price": 1.0,
        "origin_planet": "Earth"
        # no description provided
    }
    meal = meal_schema.load(data)
    assert meal.description is None
