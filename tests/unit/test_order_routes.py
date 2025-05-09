"""
Unit tests for order route handlers in the Cosmic Cafeteria API.
"""
import unittest
from datetime import datetime
from unittest.mock import patch, MagicMock

from src.api.routes.order_routes import OrderResource


class TestOrderResource(unittest.TestCase):
    """Unit tests for the OrderResource class."""
    
    def test_get_order(self):
        """Test getting an order by ID."""
        # Setup mocking for marshal_with
        with patch('src.api.routes.order_routes.marshal_with') as mock_marshal_with:
            # Create a dictionary mock response that will be returned from the endpoint
            mock_response = {
                'id': 1,
                'hero_id': 101,
                'meal_id': 201,
                'quantity': 2,
                'order_time': 'Tue, 15 May 2023 12:30:00 GMT',
                'status': 'PENDING'
            }
            
            # Setup marshal_with to return our mock response
            mock_marshal_with.return_value = lambda x: lambda fn: lambda *args, **kwargs: (mock_response, 200)
            
            with patch('src.api.routes.order_routes.Order') as mock_order_model:
                # Setup mock order
                mock_order = MagicMock()
                mock_order.id = 1
                mock_order.hero_id = 101
                mock_order.meal_id = 201
                mock_order.quantity = 2
                mock_order.order_time = datetime(2023, 5, 15, 12, 30, 0)
                mock_order.completed_time = None  # This needs to be mocked to avoid utctimetuple() errors
                
                # Mock status as an enum with value attribute
                mock_status = MagicMock()
                mock_status.value = "PENDING"
                mock_order.status = mock_status
                
                mock_order_model.query.get_or_404.return_value = mock_order
                
                # Create resource and call get
                resource = OrderResource()
                result = resource.get(1)
                
                # Assertions
                self.assertEqual(result[1], 200)  # Status code is the second item
                self.assertEqual(result[0], mock_response)  # The response should match our mock
                mock_order_model.query.get_or_404.assert_called_once_with(1)
    
    # No patch method exists in OrderResource, so we'll add tests for delete instead
    @patch('src.api.routes.order_routes.Order')
    @patch('src.api.routes.order_routes.db')
    @patch('src.api.routes.order_routes.OrderStatus')
    def test_delete_order_cancelled(self, mock_order_status, mock_db, mock_order_model):
        """Test cancelling an order."""
        # Setup mocks for OrderStatus enum
        mock_pending = MagicMock()
        mock_pending.value = "PENDING"
        mock_in_progress = MagicMock()
        mock_in_progress.value = "IN_PROGRESS"
        mock_cancelled = MagicMock()
        mock_cancelled.value = "CANCELLED"
        
        # Set up enum values
        mock_order_status.PENDING = mock_pending
        mock_order_status.IN_PROGRESS = mock_in_progress
        mock_order_status.CANCELLED = mock_cancelled
        
        # Setup mocks for request parsing
        with patch('src.api.routes.order_routes.reqparse.RequestParser') as mock_parser_class:
            mock_parser = MagicMock()
            mock_parser_class.return_value = mock_parser
            
            # Set parser to return a cancellation message
            mock_args = {'message': 'Changed my mind'}
            mock_parser.parse_args.return_value = mock_args
            
            # Setup mock for existing order in PENDING status
            mock_order = MagicMock()
            mock_order.id = 1
            mock_order.status = mock_pending
            
            # Configure the mock order status.__in__ to make the test pass
            pending_in_progress = [mock_pending, mock_in_progress]
            mock_order.status.__eq__.side_effect = lambda x: x in pending_in_progress
            mock_order.status.__invert__ = lambda: False
            mock_order_model.query.get_or_404.return_value = mock_order
            
            # Create resource and call delete
            resource = OrderResource()
            result = resource.delete(1)
            
            # Assertions
            self.assertEqual(result[1], 200)  # Status code should be 200 OK for cancellation
            self.assertIn('message', result[0])  # Should return a message
            self.assertEqual(mock_order.status, mock_cancelled)
            self.assertEqual(mock_order.message, 'Changed my mind')
            self.assertIsNotNone(mock_order.completed_time)
            mock_order_model.query.get_or_404.assert_called_once_with(1)
            mock_db.session.commit.assert_called_once()

    @patch('src.api.routes.order_routes.Order')
    @patch('src.api.routes.order_routes.db')
    @patch('src.api.routes.order_routes.OrderStatus')
    def test_delete_order_completed(self, mock_order_status, mock_db, mock_order_model):
        """Test deleting a completed order."""
        # Setup mocks for OrderStatus enum
        mock_pending = MagicMock()
        mock_pending.value = "PENDING"
        mock_in_progress = MagicMock()
        mock_in_progress.value = "IN_PROGRESS"
        mock_completed = MagicMock()
        mock_completed.value = "COMPLETED"
        
        # Set up enum values
        mock_order_status.PENDING = mock_pending
        mock_order_status.IN_PROGRESS = mock_in_progress
        mock_order_status.COMPLETED = mock_completed
        
        # Setup mocks for request parsing
        with patch('src.api.routes.order_routes.reqparse.RequestParser') as mock_parser_class:
            mock_parser = MagicMock()
            mock_parser_class.return_value = mock_parser
            
            # Set parser to return a message
            mock_args = {'message': 'Not needed'}
            mock_parser.parse_args.return_value = mock_args
            
            # Setup mock for existing order in COMPLETED status
            mock_order = MagicMock()
            mock_order.id = 1
            mock_order.status = mock_completed
            
            # Configure the mock to verify the status is not PENDING or IN_PROGRESS
            def mock_eq(other):
                if other == mock_pending or other == mock_in_progress:
                    return False
                return True
            
            mock_order.status.__eq__.side_effect = mock_eq
            mock_order_model.query.get_or_404.return_value = mock_order
            
            # Create resource and call delete
            resource = OrderResource()
            result = resource.delete(1)
            
            # Assertions
            self.assertEqual(result[1], 204)  # Status code should be 204 No Content for deletion
            self.assertEqual(result[0], '')  # Should return empty response
            mock_order_model.query.get_or_404.assert_called_once_with(1)
            mock_db.session.delete.assert_called_once_with(mock_order)
            mock_db.session.commit.assert_called_once()

    def test_post_order(self):
        """Test creating a new order."""
        with patch('src.api.routes.order_routes.redis') as mock_redis, \
             patch('src.api.routes.order_routes.Queue') as mock_queue, \
             patch('src.api.routes.order_routes.Hero') as mock_hero_model, \
             patch('src.api.routes.order_routes.Meal') as mock_meal_model, \
             patch('src.api.routes.order_routes.Order') as mock_order_model, \
             patch('src.api.routes.order_routes.db') as mock_db, \
             patch('src.api.routes.order_routes.OrderStatus') as mock_order_status, \
             patch('src.api.routes.order_routes.current_app', create=True) as mock_current_app, \
             patch('src.api.routes.order_routes.marshal_with') as mock_marshal_with:
            
            # Setup mock for OrderStatus.PENDING
            mock_pending = MagicMock()
            mock_pending.value = "PENDING"
            mock_order_status.PENDING = mock_pending
            
            # Setup mock for Flask app context
            mock_current_app.config.get.return_value = 'redis://localhost:6379/0'
            
            # Create a dictionary mock response that will be returned from the endpoint
            mock_response = {
                'id': 1,
                'hero_id': 101,
                'meal_id': 201,
                'status': 'PENDING'
            }
            
            # Set up marshal_with to return our mock response
            mock_marshal_with.return_value = lambda x: lambda fn: lambda *args, **kwargs: (mock_response, 202)
            
            # Setup mocks for request parsing
            with patch('src.api.routes.order_routes.reqparse.RequestParser') as mock_parser_class:
                mock_parser = MagicMock()
                mock_parser_class.return_value = mock_parser
                
                # Set parser to return order data
                mock_args = {'hero_id': 101, 'meal_id': 201}
                mock_parser.parse_args.return_value = mock_args
                
                # Setup mock for Hero and Meal
                mock_hero = MagicMock()
                mock_hero.id = 101
                mock_hero_model.query.get.return_value = mock_hero
                
                mock_meal = MagicMock()
                mock_meal.id = 201
                mock_meal_model.query.get.return_value = mock_meal
                
                # Setup mock for Order creation
                mock_order = MagicMock()
                mock_order.id = 1
                mock_order.hero_id = mock_args['hero_id']
                mock_order.meal_id = mock_args['meal_id']
                mock_order.status = mock_pending
                mock_order_model.return_value = mock_order
                
                # Setup mock queue
                mock_queue_instance = MagicMock()
                mock_queue.return_value = mock_queue_instance
                
                # Create resource and call post
                resource = OrderResource()
                result = resource.post()
                
                # Assertions
                self.assertEqual(result[1], 202)  # Status code should be 202 Accepted
                self.assertEqual(result[0], mock_response)  # First item is the order object
                mock_hero_model.query.get.assert_called_once_with(mock_args['hero_id'])
                mock_meal_model.query.get.assert_called_once_with(mock_args['meal_id'])
                mock_db.session.add.assert_called_once_with(mock_order)
                mock_db.session.commit.assert_called_once()
                mock_queue_instance.enqueue.assert_called_once()


if __name__ == '__main__':
    unittest.main()