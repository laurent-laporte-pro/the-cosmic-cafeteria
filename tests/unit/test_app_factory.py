"""
Unit tests for the application factory.
"""
import unittest
from unittest.mock import patch, MagicMock

from src.api import create_app


class TestAppFactory(unittest.TestCase):
    """Unit tests for the application factory function."""

    def test_create_app_default_config(self):
        """Test creating app with default configuration."""
        with patch('src.api.db') as mock_db, \
             patch('src.api.register_routes') as mock_register_routes, \
             patch('src.api.Migrate') as mock_migrate:
            
            app = create_app()
            
            # Assert that the app was created with expected config
            self.assertEqual(app.config['SQLALCHEMY_TRACK_MODIFICATIONS'], False)
            self.assertEqual(app.config['DEBUG'], False)
            self.assertTrue('SECRET_KEY' in app.config)
            self.assertTrue('SQLALCHEMY_DATABASE_URI' in app.config)
            
            # Assert that dependencies were initialized properly
            mock_db.init_app.assert_called_once_with(app)
            mock_register_routes.assert_called_once_with(app)
            mock_migrate.assert_called_once()
    
    def test_create_app_custom_config(self):
        """Test creating app with custom configuration."""
        custom_config = {
            'SQLALCHEMY_DATABASE_URI': 'sqlite:///test.db',
            'TESTING': True,
            'DEBUG': True,
            'SECRET_KEY': 'test-key'
        }
        
        with patch('src.api.db') as mock_db, \
             patch('src.api.register_routes') as mock_register_routes, \
             patch('src.api.Migrate') as mock_migrate:
            
            app = create_app(custom_config)
            
            # Assert that the app was created with expected config
            self.assertEqual(app.config['SQLALCHEMY_DATABASE_URI'], 'sqlite:///test.db')
            self.assertEqual(app.config['TESTING'], True)
            self.assertEqual(app.config['DEBUG'], True)
            self.assertEqual(app.config['SECRET_KEY'], 'test-key')
            
            # Assert that dependencies were initialized properly
            mock_db.init_app.assert_called_once_with(app)
            mock_register_routes.assert_called_once_with(app)
            mock_migrate.assert_called_once()
    
    @patch('src.api.db')
    def test_init_db_command(self, mock_db):
        """Test the init-db CLI command."""
        app = create_app({'TESTING': True})
        runner = app.test_cli_runner()
        
        # Run the init-db command
        result = runner.invoke(args=['init-db'])
        
        # Assert command output and behavior
        self.assertIn('Initialized the database', result.output)
        mock_db.create_all.assert_called_once()


if __name__ == '__main__':
    unittest.main()