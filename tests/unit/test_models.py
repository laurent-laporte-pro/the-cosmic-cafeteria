"""
Unit tests for database models in the Cosmic Cafeteria API.
"""
import unittest
from unittest.mock import patch, MagicMock

from src.api.models import Hero, Allergy, Meal, Ingredient, Order, OrderStatus


class TestHeroModel(unittest.TestCase):
    """Unit tests for the Hero model."""
    
    def test_hero_init(self):
        """Test hero initialization with proper attributes."""
        hero = Hero(name="Test Hero", planet="Test Planet")
        
        self.assertEqual(hero.name, "Test Hero")
        self.assertEqual(hero.planet, "Test Planet")
        self.assertEqual(hero.orders, [])
        self.assertEqual(hero.allergies, [])
        
    def test_hero_repr(self):
        """Test the string representation of a hero."""
        hero = Hero(id=1, name="Test Hero", planet="Test Planet")
        
        expected = "<Hero(id=1, name='Test Hero', planet='Test Planet')>"
        self.assertEqual(repr(hero), expected)


class TestAllergyModel(unittest.TestCase):
    """Unit tests for the Allergy model."""
    
    def test_allergy_init(self):
        """Test allergy initialization."""
        allergy = Allergy(name="test_allergy")
        
        self.assertEqual(allergy.name, "test_allergy")
    
    def test_allergy_repr(self):
        """Test the string representation of an allergy."""
        allergy = Allergy(name="test_allergy")
        
        expected = "<Allergy(name='test_allergy')>"
        self.assertEqual(repr(allergy), expected)


class TestOrderStatus(unittest.TestCase):
    """Unit tests for the OrderStatus enum."""
    
    def test_order_status_values(self):
        """Test order status enum values."""
        self.assertEqual(OrderStatus.PENDING.value, "pending")
        self.assertEqual(OrderStatus.IN_PROGRESS.value, "in_progress")
        self.assertEqual(OrderStatus.COMPLETED.value, "completed")
        self.assertEqual(OrderStatus.CANCELLED.value, "cancelled")


if __name__ == '__main__':
    unittest.main()