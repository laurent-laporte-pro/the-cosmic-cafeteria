import pytest
from sqlalchemy.orm.attributes import flag_modified
from api.models.meal import Meal



def test_create_meal(session, meal):
    retrieved = session.get(Meal, meal.id)
    assert retrieved.name == "Starburger"
    assert "Beef" in retrieved.ingredients
    assert retrieved.origin_planet == "Mars"
    assert retrieved.description is not None

def test_update_meal(session, meal):
    meal.price = 15.50
    meal.ingredients.append("MeteorDust")
    flag_modified(meal, "ingredients")  # Important!
    session.commit()

    updated = session.get(Meal, meal.id)
    assert updated.price == 15.50
    assert "MeteorDust" in updated.ingredients

def test_delete_meal(session, meal):
    session.delete(meal)
    session.commit()
    assert session.get(Meal, meal.id) is None
