"""
Unit tests for meal route handlers in the Cosmic Cafeteria API.
"""
import unittest
from unittest.mock import patch, MagicMock

from src.api.routes.meal_routes import MealListResource, MealResource, MealIngredientsResource
from src.api.models import Meal, Ingredient


class TestMealListResource(unittest.TestCase):
    """Unit tests for the MealListResource class."""
    
    @patch('src.api.routes.meal_routes.Meal')
    def test_get_meals(self, mock_meal_model):
        """Test getting a list of meals."""
        # Setup mock
        mock_meal1 = MagicMock()
        mock_meal1.id = 1
        mock_meal1.name = "Mock Meal 1"
        mock_meal1.description = "Description 1"
        mock_meal1.price = 9.99
        mock_meal1.origin_planet = "Mars"
        
        mock_meal2 = MagicMock()
        mock_meal2.id = 2
        mock_meal2.name = "Mock Meal 2"
        mock_meal2.description = "Description 2"
        mock_meal2.price = 14.99
        mock_meal2.origin_planet = "Venus"
        
        mock_meal_model.query.all.return_value = [mock_meal1, mock_meal2]
        
        # Create resource and call get
        resource = MealListResource()
        result = resource.get()
        
        # Assertions
        self.assertEqual(result[1], 200)  # Status code is the second item in the tuple
        self.assertEqual(len(result[0]), 2)  # Result is the first item in the tuple
        mock_meal_model.query.all.assert_called_once()
    
    @patch('src.api.routes.meal_routes.Meal')
    @patch('src.api.routes.meal_routes.db')
    def test_post_meal(self, mock_db, mock_meal_model):
        """Test creating a new meal."""
        # Setup mock for request parsing
        with patch('src.api.routes.meal_routes.reqparse.RequestParser') as mock_parser_class:
            mock_parser = MagicMock()
            mock_parser_class.return_value = mock_parser
            
            # Set parser to return meal data
            mock_args = {
                'name': 'New Meal', 
                'description': 'New Description', 
                'price': 12.99, 
                'origin_planet': 'Mars'  # Changed from vegan to origin_planet
            }
            mock_parser.parse_args.return_value = mock_args
            
            # Setup mock for Meal creation
            mock_meal = MagicMock()
            mock_meal.id = 1
            mock_meal.name = mock_args['name']
            mock_meal.description = mock_args['description']
            mock_meal.price = mock_args['price']
            mock_meal.origin_planet = mock_args['origin_planet']
            mock_meal_model.return_value = mock_meal
            
            # Create resource and call post
            resource = MealListResource()
            result = resource.post()
            
            # Assertions
            self.assertEqual(result[1], 201)  # Status code should be 201 Created
            # With Flask-RESTful marshal, the result will be a dictionary
            self.assertEqual(result[0]['name'], 'New Meal')
            self.assertEqual(result[0]['description'], 'New Description')
            self.assertEqual(result[0]['price'], 12.99)
            self.assertEqual(result[0]['origin_planet'], 'Mars')
            mock_db.session.add.assert_called_once_with(mock_meal)
            mock_db.session.commit.assert_called_once()


class TestMealResource(unittest.TestCase):
    """Unit tests for the MealResource class."""
    
    @patch('src.api.routes.meal_routes.Meal')
    def test_get_meal(self, mock_meal_model):
        """Test getting a meal by ID."""
        # Setup mock
        mock_meal = MagicMock()
        mock_meal.id = 1
        mock_meal.name = "Test Meal"
        mock_meal.description = "Test Description"
        mock_meal.price = 10.99
        mock_meal.origin_planet = "Earth"
        
        mock_meal_model.query.get_or_404.return_value = mock_meal
        
        # Create resource and call get
        resource = MealResource()
        result = resource.get(1)
        
        # Assertions
        self.assertEqual(result[1], 200)  # Status code should be 200 OK
        # Marshal will convert the object to a dict, so compare dict values
        self.assertEqual(result[0]['id'], 1)
        self.assertEqual(result[0]['name'], "Test Meal")
        mock_meal_model.query.get_or_404.assert_called_once_with(1)


if __name__ == '__main__':
    unittest.main()