import pytest
from marshmallow import ValidationError
from api.models.hero import Hero



def test_hero_schema_valid_input(hero_schema):
    input_data = {
        "name": "Thor",
        "planet": "Asgard",
        "allergies": ["Iron", "Dust"]
    }

    result = hero_schema.load(input_data)
    assert isinstance(result, Hero)
    assert result.name == "Thor"
    assert result.planet == "Asgard"
    assert result.allergies == ["Iron", "Dust"]

def test_hero_schema_missing_required_fields(hero_schema):
    input_data = {
        "planet": "Asgard"
        # Missing name
    }

    with pytest.raises(ValidationError) as exc_info:
        hero_schema.load(input_data)

    errors = exc_info.value.messages
    assert "name" in errors
    assert errors["name"][0] == "Name is required."

def test_hero_schema_allergies_default(hero_schema):
    input_data = {
        "name": "Hulk",
        "planet": "Sakaar"
        # Missing allergies
    }

    result = hero_schema.load(input_data)
    assert result.allergies == []

def test_hero_schema_field_length_validation(hero_schema):
    input_data = {
        "name": "A" * 101,  # Too long
        "planet": "Asgard"
    }

    with pytest.raises(ValidationError) as exc_info:
        hero_schema.load(input_data)

    assert "name" in exc_info.value.messages

def test_hero_schema_dump(hero_schema):
    hero = Hero(name="name_example", planet="planet_examplee", allergies=["alg_example"])
    serialized = hero_schema.dump(hero)

    assert serialized["name"] == "name_example"
    assert serialized["planet"] == "planet_examplee"
    assert serialized["allergies"] == ["alg_example"]
