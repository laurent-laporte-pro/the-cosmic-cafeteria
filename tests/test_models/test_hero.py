import pytest
from api.models.hero import Hero
from sqlalchemy.orm.attributes import flag_modified


def test_create_hero(session):
    hero = Hero(name="Superman", planet="Krypton", allergies=["Kryptonite"])
    session.add(hero)
    session.commit()

    assert hero.id is not None
    assert hero.name == "Superman"
    assert hero.planet == "Krypton"
    assert "Kryptonite" in hero.allergies


def test_read_hero(hero):
    assert hero.name == "Thor"
    assert hero.planet == "Asgard"
    assert "Iron" in hero.allergies


def test_update_hero(session, hero):
    hero.planet = "Example"
    hero.allergies.append("Alxm")
    flag_modified(hero, "allergies") 
    session.commit()
    updated = session.get(Hero, hero.id)
    assert updated.planet == "Example"
    assert "Alxm" in updated.allergies


def test_delete_hero(session, hero):
    hero_id = hero.id
    session.delete(hero)
    session.commit()

    deleted = session.get(Hero, hero_id)
    assert deleted is None
