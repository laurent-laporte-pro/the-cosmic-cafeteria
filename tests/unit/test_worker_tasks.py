"""
Unit tests for worker tasks in the Cosmic Cafeteria.
"""
import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime


class TestProcessOrder(unittest.TestCase):
    """Test the process_order task."""
    
    def setUp(self):
        """Set up before each test"""
        # Core patches
        self.create_app_patcher = patch('src.api.create_app')
        self.mock_create_app = self.create_app_patcher.start()
        
        # Setup app context
        self.mock_app = MagicMock()
        self.mock_app_context = MagicMock()
        self.mock_app.app_context.return_value = self.mock_app_context
        self.mock_create_app.return_value = self.mock_app
        
        # We also need to patch the module-level import
        self.import_module_patcher = patch('importlib.import_module')
        self.mock_import_module = self.import_module_patcher.start()
        
    def tearDown(self):
        """Clean up after each test"""
        self.create_app_patcher.stop()
        self.import_module_patcher.stop()
    
    def test_process_order_success(self):
        """Test processing an order that completes successfully."""
        # Mock database models
        with patch('src.worker.tasks.Order') as mock_order_model, \
             patch('src.worker.tasks.Hero') as mock_hero_model, \
             patch('src.worker.tasks.Meal') as mock_meal_model, \
             patch('src.worker.tasks.db') as mock_db, \
             patch('src.worker.tasks.OrderStatus') as mock_order_status, \
             patch('src.worker.tasks.time') as mock_time, \
             patch('src.worker.tasks.datetime') as mock_datetime:
        
            # Set up mock order status
            mock_in_progress = MagicMock()
            mock_in_progress.value = "IN_PROGRESS"
            mock_completed = MagicMock()
            mock_completed.value = "COMPLETED"
            mock_order_status.IN_PROGRESS = mock_in_progress
            mock_order_status.COMPLETED = mock_completed
            
            # Set up mock datetime
            mock_now = datetime(2023, 6, 1, 12, 0, 0)
            mock_datetime.utcnow.return_value = mock_now
            
            # Setup mock order
            mock_order = MagicMock()
            mock_order.id = 1
            mock_order.hero_id = 101
            mock_order.meal_id = 201
            mock_order_model.query.get.return_value = mock_order
            
            # Setup mock hero with allergies
            mock_hero = MagicMock()
            mock_allergy1 = MagicMock()
            mock_allergy1.name = 'gluten'
            mock_allergy2 = MagicMock()
            mock_allergy2.name = 'dairy'
            mock_hero.allergies = [mock_allergy1, mock_allergy2]
            mock_hero_model.query.get.return_value = mock_hero
            
            # Setup mock meal with ingredients that don't conflict with allergies
            mock_meal = MagicMock()
            mock_ingredient1 = MagicMock()
            mock_ingredient1.name = 'wheat'  # Not exact match with gluten
            mock_ingredient2 = MagicMock()
            mock_ingredient2.name = 'tomato'  # Not an allergen
            mock_meal.ingredients = [mock_ingredient1, mock_ingredient2]
            mock_meal_model.query.get.return_value = mock_meal
            
            # Now import and call the function
            from src.worker.tasks import process_order
            result = process_order(1)
            
            # Assertions
            self.assertIsNotNone(result)
            self.assertEqual(result['order_id'], 1)
            self.assertEqual(result['status'], 'completed')
            
            # Verify correct state changes
            self.assertEqual(mock_order.status, mock_completed)
            self.assertEqual(mock_order.completed_time, mock_now)
            mock_db.session.commit.assert_called()
            mock_time.sleep.assert_called_once_with(5)
    
    def test_process_order_with_allergies(self):
        """Test processing an order that fails due to allergies."""
        # Mock database models
        with patch('src.worker.tasks.Order') as mock_order_model, \
             patch('src.worker.tasks.Hero') as mock_hero_model, \
             patch('src.worker.tasks.Meal') as mock_meal_model, \
             patch('src.worker.tasks.db') as mock_db, \
             patch('src.worker.tasks.OrderStatus') as mock_order_status, \
             patch('src.worker.tasks.time') as mock_time, \
             patch('src.worker.tasks.datetime') as mock_datetime:
        
            # Set up mock order status
            mock_in_progress = MagicMock()
            mock_in_progress.value = "IN_PROGRESS"
            mock_cancelled = MagicMock()
            mock_cancelled.value = "CANCELLED"
            mock_order_status.IN_PROGRESS = mock_in_progress
            mock_order_status.CANCELLED = mock_cancelled
            
            # Set up mock datetime
            mock_now = datetime(2023, 6, 1, 12, 0, 0)
            mock_datetime.utcnow.return_value = mock_now
            
            # Setup mock order
            mock_order = MagicMock()
            mock_order.id = 1
            mock_order.hero_id = 101
            mock_order.meal_id = 201
            mock_order_model.query.get.return_value = mock_order
            
            # Setup mock hero with allergies
            mock_hero = MagicMock()
            mock_allergy1 = MagicMock()
            mock_allergy1.name = 'PEANUTS'  # Using uppercase to test case insensitivity
            mock_allergy2 = MagicMock()
            mock_allergy2.name = 'dairy'
            mock_hero.allergies = [mock_allergy1, mock_allergy2]
            mock_hero_model.query.get.return_value = mock_hero
            
            # Setup mock meal with ingredients that include allergens
            mock_meal = MagicMock()
            mock_ingredient1 = MagicMock()
            mock_ingredient1.name = 'wheat'
            mock_ingredient2 = MagicMock()
            mock_ingredient2.name = 'peanuts'  # This will trigger the allergy
            mock_meal.ingredients = [mock_ingredient1, mock_ingredient2]
            mock_meal_model.query.get.return_value = mock_meal
            
            # Now import and call the function
            from src.worker.tasks import process_order
            result = process_order(1)
            
            # Assertions
            self.assertIsNotNone(result)
            self.assertEqual(result['order_id'], 1)
            self.assertEqual(result['status'], 'cancelled')
            self.assertIn('reason', result)
            self.assertIn('peanuts', result['reason'].lower())  # Case insensitive check
            
            # Verify correct state changes
            self.assertEqual(mock_order.status, mock_cancelled)
            self.assertEqual(mock_order.completed_time, mock_now)
            self.assertIn('allergies', str(mock_order.message).lower())  # Case insensitive check
            mock_db.session.commit.assert_called()
    
    def test_process_order_not_found(self):
        """Test processing a non-existent order."""
        # Mock database models
        with patch('src.worker.tasks.Order') as mock_order_model, \
             patch('src.worker.tasks.logger') as mock_logger:
            
            # Setup mock order to return None (not found)
            mock_order_model.query.get.return_value = None
            
            # Now import and call the function
            from src.worker.tasks import process_order
            result = process_order(999)
            
            # Assertions
            self.assertIsNone(result)
            mock_logger.error.assert_called_once()


if __name__ == '__main__':
    unittest.main()
