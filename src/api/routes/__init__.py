"""
This module contains the API endpoints for the Cosmic Cafeteria API.

The routes are base on Flask-RESTFul.
"""
from flask import jsonify
from flask_restful import Api

from .hero_routes import HeroListResource, HeroResource, HeroAllergiesResource
from .meal_routes import MealListResource, MealResource, MealIngredientsResource
from .order_routes import OrderResource

def register_routes(app):
    api = Api(app)
    
    # Hero routes
    api.add_resource(HeroListResource, '/heroes')
    api.add_resource(HeroResource, '/heroes/<int:hero_id>')
    api.add_resource(HeroAllergiesResource, '/heroes/<int:hero_id>/allergies')
    
    # Meal routes
    api.add_resource(MealListResource, '/meals')
    api.add_resource(MealResource, '/meals/<int:meal_id>')
    api.add_resource(MealIngredientsResource, '/meals/<int:meal_id>/ingredients')
    
    # Order routes
    api.add_resource(OrderResource, '/orders', '/orders/<int:order_id>')
    
    # API Documentation
    @app.route('/api/docs')
    def api_docs():
        """Generate a list of all API endpoints."""
        endpoints = []
        for rule in app.url_map.iter_rules():
            # Exclude static and documentation endpoints
            if not rule.rule.startswith('/static') and rule.rule != '/api/docs':
                methods = ','.join(sorted(rule.methods - {'HEAD', 'OPTIONS'}))
                endpoints.append({
                    'url': rule.rule,
                    'methods': methods,
                    'endpoint': rule.endpoint
                })
        
        # Sort endpoints by URL for better readability
        endpoints.sort(key=lambda e: e['url'])
        return jsonify({
            'api_version': '1.0',
            'endpoints': endpoints
        })
    
    return api
