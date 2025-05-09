"""
Test fixtures for the Cosmic Cafeteria API unit tests.
"""
import os
import tempfile
import pytest
from flask import Flask
from unittest.mock import MagicMock, patch

from src.api import create_app
from src.api.models import db as _db


@pytest.fixture(scope="session")
def app():
    """Create a Flask app context for the tests."""
    # Create a temporary file for SQLite database
    db_fd, db_path = tempfile.mkstemp()
    
    app = create_app({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': f'sqlite:///{db_path}',
        'SQLALCHEMY_TRACK_MODIFICATIONS': False,
        'SECRET_KEY': 'test-secret-key',
        'DEBUG': False,
    })

    # Establish application context
    with app.app_context():
        # Create all tables in the test database
        _db.create_all()
        
        yield app
        
        # Clean up after tests by dropping all tables
        _db.session.remove()
        _db.drop_all()
    
    # Close and remove the temporary database file
    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture(scope="function")
def client(app):
    """Create a test client for the Flask app."""
    return app.test_client()


@pytest.fixture(scope="function")
def runner(app):
    """Create a test CLI runner for Flask commands."""
    return app.test_cli_runner()


@pytest.fixture(scope="function")
def session(app):
    """Create a new database session for a test."""
    with app.app_context():
        # Start a transaction
        connection = _db.engine.connect()
        transaction = connection.begin()
        
        # Get the session
        session = _db.session
        
        yield session
        
        # Rollback the transaction and close connections
        session.close()
        transaction.rollback()
        connection.close()