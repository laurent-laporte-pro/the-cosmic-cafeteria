"""
Unit tests for route handlers in the Cosmic Cafeteria API.

These tests focus on testing route handler methods in isolation from HTTP.
"""
import unittest
from unittest.mock import patch, MagicMock

from src.api.routes.hero_routes import HeroListResource, HeroResource
from src.api.models import Hero, Allergy


class TestHeroListResource(unittest.TestCase):
    """Unit tests for the HeroListResource class."""
    
    @patch('src.api.routes.hero_routes.Hero')
    def test_get_heroes(self, mock_hero_model):
        """Test getting a list of heroes."""
        # Setup mock
        mock_hero1 = MagicMock()
        mock_hero1.id = 1
        mock_hero1.name = "Mock Hero 1"
        mock_hero1.planet = "Mock Planet 1"
        
        mock_hero2 = MagicMock()
        mock_hero2.id = 2
        mock_hero2.name = "Mock Hero 2"
        mock_hero2.planet = "Mock Planet 2"
        
        mock_hero_model.query.all.return_value = [mock_hero1, mock_hero2]
        
        # Create resource and call get
        resource = HeroListResource()
        result = resource.get()
        
        # Assertions
        self.assertEqual(result[1], 200)  # Status code is the second item
        self.assertEqual(len(result[0]), 2)  # Result list is the first item
        mock_hero_model.query.all.assert_called_once()
    
    def test_post_hero(self):
        """Test creating a new hero."""
        with patch('src.api.routes.hero_routes.Hero') as mock_hero_model, \
             patch('src.api.routes.hero_routes.db') as mock_db, \
             patch('src.api.routes.hero_routes.marshal_with') as mock_marshal_with:
            
            # Create a dictionary mock response that will be returned from the endpoint
            mock_response = {
                'id': 1,
                'name': 'New Hero',
                'planet': 'New Planet'
            }
            
            # Set up marshal_with to return our mock response
            mock_marshal_with.return_value = lambda x: lambda fn: lambda *args, **kwargs: (mock_response, 201)
            
            # Setup mock for request parsing
            with patch('src.api.routes.hero_routes.reqparse.RequestParser') as mock_parser_class:
                mock_parser = MagicMock()
                mock_parser_class.return_value = mock_parser
                
                # Set parser to return hero data
                mock_args = {'name': 'New Hero', 'planet': 'New Planet'}
                mock_parser.parse_args.return_value = mock_args
                
                # Setup mock for Hero creation
                mock_hero = MagicMock()
                mock_hero.id = 1
                mock_hero.name = mock_args['name']
                mock_hero.planet = mock_args['planet']
                mock_hero_model.return_value = mock_hero
                
                # Create resource and call post
                resource = HeroListResource()
                result = resource.post()
                
                # Assertions
                self.assertEqual(result[1], 201)  # Status code should be 201 Created
                self.assertEqual(result[0], mock_response)  # Compare to our mock response
                mock_db.session.add.assert_called_once_with(mock_hero)
                mock_db.session.commit.assert_called_once()


class TestHeroResource(unittest.TestCase):
    """Unit tests for the HeroResource class."""
    
    def test_get_hero(self):
        """Test getting a hero by ID."""
        with patch('src.api.routes.hero_routes.Hero') as mock_hero_model, \
             patch('src.api.routes.hero_routes.marshal_with') as mock_marshal_with:
            
            # Create a dictionary mock response that will be returned from the endpoint
            mock_response = {
                'id': 1,
                'name': 'Test Hero',
                'planet': 'Test Planet',
                'allergies': [],
                'orders': []
            }
            
            # Set up marshal_with to return our mock response
            mock_marshal_with.return_value = lambda x: lambda fn: lambda *args, **kwargs: (mock_response, 200)
            
            # Setup mock hero
            mock_hero = MagicMock()
            mock_hero.id = 1
            mock_hero.name = "Test Hero"
            mock_hero.planet = "Test Planet"
            mock_hero.allergies = []
            
            # Setup mock for orders to avoid datetime errors
            mock_hero.orders = []
            
            mock_hero_model.query.get_or_404.return_value = mock_hero
            
            # Create resource and call get
            resource = HeroResource()
            result = resource.get(1)
            
            # Assertions
            self.assertEqual(result[1], 200)  # Status code is the second item
            self.assertEqual(result[0], mock_response)  # Compare to our mock response dictionary
            mock_hero_model.query.get_or_404.assert_called_once_with(1)


if __name__ == '__main__':
    unittest.main()