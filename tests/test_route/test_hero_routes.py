import pytest
from api.models.hero import Hero

def test_create_hero(client, session, example_hero_payload):
    response = client.post("api/heroes/", json=example_hero_payload)
    assert response.status_code == 201
    data = response.get_json()
    assert data["success"] is True
    assert data["data"]["name"] == example_hero_payload["name"]
    assert "id" in data["data"]

def test_get_hero(client, session, example_hero_payload):
    hero = Hero(**example_hero_payload)
    session.add(hero)
    session.commit()

    response = client.get(f"api/heroes/{hero.id}")
    assert response.status_code == 200
    data = response.get_json()
    assert data["success"] is True
    assert data["data"]["name"] == example_hero_payload["name"]

def test_get_all_heros(client, session, example_hero_payload):
    hero = Hero(**example_hero_payload)
    session.add(hero)
    session.commit()

    response = client.get("api/heroes/")
    assert response.status_code == 200
    data = response.get_json()
    assert data["success"] is True
    assert isinstance(data["data"], list)
    assert any(h["name"] == example_hero_payload["name"] for h in data["data"])

def test_update_hero(client, session, example_hero_payload):
    hero = Hero(**example_hero_payload)
    session.add(hero)
    session.commit()

    update_data = {"planet": "Mars", "allergies": ["Dust", "Pollen"]}

    response = client.put(f"api/heroes/{hero.id}", json=update_data)
    assert response.status_code == 200
    data = response.get_json()
    assert data["success"] is True
    assert data["data"]["planet"] == "Mars"
    assert "Pollen" in data["data"]["allergies"]

def test_delete_hero(client, session, example_hero_payload):
    hero = Hero(**example_hero_payload)
    session.add(hero)
    session.commit()

    response = client.delete(f"api/heroes/{hero.id}")
    assert response.status_code in (200, 204)

    deleted_hero = session.get(Hero, hero.id)
    assert deleted_hero is None
