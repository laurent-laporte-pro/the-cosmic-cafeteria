# SPDX-FileCopyrightText: 2025-present Laurent LAPORTE <laurent.laporte.pro@gmail.com>
#
# SPDX-License-Identifier: MIT

"""
The Cosmic Cafeteria API.

This is the main entry point for the API application.
"""
import os
from flask import Flask
from flask_migrate import Migrate

from .models import db
from .routes import register_routes


def create_app(config=None):
    """Create and configure the Flask application."""
    app = Flask(__name__)
    
    # Load default configuration
    app.config.from_mapping(
        # SQLAlchemy configuration
        SQLALCHEMY_DATABASE_URI=os.environ.get(
            'DATABASE_URL', 'postgresql://user:password@tcc-db:5432/cosmic_cafeteria'
        ),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        
        # Additional configuration settings
        SECRET_KEY=os.environ.get('SECRET_KEY', 'dev-secret-key'),
        DEBUG=os.environ.get('FLASK_DEBUG', 'False').lower() == 'true',
    )
    
    # Override with any provided configuration
    if config:
        app.config.from_mapping(config)
    
    # Initialize database
    db.init_app(app)
    
    # Initialize migrations
    Migrate(app, db)
    
    # Register API routes
    register_routes(app)
    
    # Create a CLI command to initialize the database
    @app.cli.command('init-db')
    def init_db_command():
        """Clear existing data and create new tables."""
        with app.app_context():
            db.create_all()
        print('Initialized the database.')
    
    return app
