"""
Unit tests for the schema definitions in the Cosmic Cafeteria API.
"""
import unittest
from datetime import datetime
from unittest.mock import MagicMock, patch
from enum import Enum

from src.api.schemas import (
    OrderStatusField, hero_schema, hero_create_schema,
    allergy_schema, hero_allergy_update_schema, 
    ingredient_schema, meal_ingredient_update_schema,
    meal_schema, meal_create_schema, order_schema,
    hero_detail_schema, meal_detail_schema
)


class TestOrderStatusField(unittest.TestCase):
    """Test the custom OrderStatusField class."""
    
    def test_format_with_enum_value(self):
        """Test formatting an enum value."""
        # Create a field
        field = OrderStatusField()
        
        # Create a mock enum object with a value property
        mock_enum = MagicMock()
        mock_enum.value = "PENDING"
        
        # Test with mock enum value
        result = field.format(mock_enum)
        
        # Assert result matches the enum's value property
        self.assertEqual(result, "PENDING")
    
    def test_format_with_none(self):
        """Test formatting None."""
        field = OrderStatusField()
        
        result = field.format(None)
        
        self.assertIsNone(result)


class TestHeroSchema(unittest.TestCase):
    """Test the hero schemas."""
    
    def test_hero_schema_structure(self):
        """Verify the hero_schema has the expected fields."""
        expected_keys = {'id', 'name', 'planet'}
        self.assertEqual(set(hero_schema.keys()), expected_keys)
    
    def test_hero_create_schema_structure(self):
        """Verify the hero_create_schema has the expected fields."""
        expected_keys = {'name', 'planet'}
        self.assertEqual(set(hero_create_schema.keys()), expected_keys)
    
    def test_hero_detail_schema_structure(self):
        """Verify the hero_detail_schema has additional fields."""
        expected_base_keys = {'id', 'name', 'planet'}
        expected_additional_keys = {'allergies', 'orders'}
        
        # Check that all base keys are included
        for key in expected_base_keys:
            self.assertIn(key, hero_detail_schema)
        
        # Check that additional keys are included
        for key in expected_additional_keys:
            self.assertIn(key, hero_detail_schema)


class TestMealSchema(unittest.TestCase):
    """Test the meal schemas."""
    
    def test_meal_schema_structure(self):
        """Verify the meal_schema has the expected fields."""
        expected_keys = {'id', 'name', 'price', 'origin_planet', 'description'}
        self.assertEqual(set(meal_schema.keys()), expected_keys)
    
    def test_meal_create_schema_structure(self):
        """Verify the meal_create_schema has the expected fields."""
        expected_keys = {'name', 'price', 'origin_planet', 'description'}
        self.assertEqual(set(meal_create_schema.keys()), expected_keys)
    
    def test_meal_detail_schema_structure(self):
        """Verify the meal_detail_schema has additional fields."""
        expected_base_keys = {'id', 'name', 'price', 'origin_planet', 'description'}
        expected_additional_keys = {'ingredients', 'ordered_by'}
        
        # Check that all base keys are included
        for key in expected_base_keys:
            self.assertIn(key, meal_detail_schema)
        
        # Check that additional keys are included
        for key in expected_additional_keys:
            self.assertIn(key, meal_detail_schema)


class TestOrderSchema(unittest.TestCase):
    """Test the order schema."""
    
    def test_order_schema_structure(self):
        """Verify the order_schema has the expected fields."""
        expected_keys = {
            'id', 'status', 'message', 'order_time', 'completed_time', 
            'hero_id', 'meal_id', 'hero', 'meal'
        }
        self.assertEqual(set(order_schema.keys()), expected_keys)


class TestIngredientAndAllergySchemas(unittest.TestCase):
    """Test the ingredient and allergy schemas."""
    
    def test_allergy_schema(self):
        """Verify the allergy_schema has the expected fields."""
        self.assertIn('name', allergy_schema)
    
    def test_ingredient_schema(self):
        """Verify the ingredient_schema has the expected fields."""
        self.assertIn('name', ingredient_schema)
    
    def test_hero_allergy_update_schema(self):
        """Verify the hero_allergy_update_schema has the expected fields."""
        self.assertIn('allergies', hero_allergy_update_schema)
    
    def test_meal_ingredient_update_schema(self):
        """Verify the meal_ingredient_update_schema has the expected fields."""
        self.assertIn('ingredients', meal_ingredient_update_schema)


if __name__ == '__main__':
    unittest.main()