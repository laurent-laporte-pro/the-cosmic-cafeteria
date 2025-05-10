"""
This module contains the API endpoints for the Cosmic Cafeteria API.

The routes are base on Flask-RESTFul.
"""

from .hero_routes import hero_blueprint
from .meal_routes import meal_blueprint
from .order_routes import order_blueprint