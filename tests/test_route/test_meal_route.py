import pytest
from api.models.meal import Meal


def test_create_meal(client, session, example):
    response = client.post("api/meals/", json=example)
    assert response.status_code == 201
    data = response.get_json()
    assert data["success"] is True
    assert data["data"]["name"] == example["name"]
    assert "id" in data["data"]

def test_get_meal(client, session, example):
    meal = Meal(**example)
    session.add(meal)
    session.commit()

    response = client.get(f"api/meals/{meal.id}")
    assert response.status_code == 200
    data = response.get_json()
    assert data["success"] is True
    assert data["data"]["name"] == example["name"]

def test_get_all_meals(client, session, example):
    meal = Meal(**example)
    session.add(meal)
    session.commit()

    response = client.get("api/meals/")
    assert response.status_code == 200
    data = response.get_json()
    assert data["success"] is True
    assert isinstance(data["data"], list)
    assert any(m["name"] == example["name"] for m in data["data"])

def test_update_meal(client, session, example):
    meal = Meal(**example)
    session.add(meal)
    session.commit()

    update_data = {"price": 20.00, "description": "Updated description"}

    response = client.put(f"api/meals/{meal.id}", json=update_data)
    assert response.status_code == 200
    data = response.get_json()
    assert data["success"] is True
    assert data["data"]["price"] == 20.00
    assert data["data"]["description"] == "Updated description"

def test_delete_meal(client, session, example):
    meal = Meal(**example)
    session.add(meal)
    session.commit()

    response = client.delete(f"api/meals/{meal.id}")
    assert response.status_code in (200, 204)

    deleted_meal = session.get(Meal, meal.id)
    assert deleted_meal is None
