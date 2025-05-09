"""
Meal routes for the Cosmic Cafeteria API.

This module implements CRUD operations for meals and a dedicated endpoint for managing meal ingredients.
"""
from flask import request
from flask_restful import Resource, marshal_with, reqparse, fields, inputs

from ..models import Meal, Ingredient, db
from ..schemas import meal_schema, meal_create_schema, meal_detail_schema, ingredient_schema, meal_ingredient_update_schema


class MealListResource(Resource):

    
    @marshal_with(meal_schema)
    def get(self):
        """Get all meals."""
        meals = Meal.query.all()
        return meals, 200
    
    @marshal_with(meal_schema)
    def post(self):
        """Create a new meal."""
        parser = reqparse.RequestParser()
        parser.add_argument(
            'name', 
            type=str, 
            required=True, 
            help='feild name is required',
            location=['form', 'json'],
            trim=True,
            nullable=False
        )
        parser.add_argument(
            'price', 
            type=float, 
            required=True, 
            help='feild price is required',
            location=['form', 'json']
        )
        parser.add_argument(
            'origin_planet', 
            type=str, 
            required=True, 
            help='feild origin_planet is required',
            location=['form', 'json'],
            trim=True,
            nullable=False
        )
        parser.add_argument(
            'description', 
            type=str,
            location=['form', 'json'],
            trim=True
        )
        
        args = parser.parse_args()
        
        # Additional validation
        if len(args['name']) < 2:
            return {'message': 'Meal name must be at least 2 characters'}, 400
        
        if len(args['name']) > 100:
            return {'message': 'Meal name cannot exceed 100 characters'}, 400
            
        if args['price'] <= 0:
            return {'message': 'Meal price must be greater than 0'}, 400
            
        if len(args['origin_planet']) < 2:
            return {'message': 'Origin planet must be at least 2 characters'}, 400
            
        if len(args['origin_planet']) > 50:
            return {'message': 'Origin planet cannot exceed 50 characters'}, 400
        
        # Create meal
        meal = Meal(
            name=args['name'],
            price=args['price'],
            origin_planet=args['origin_planet'],
            description=args.get('description')
        )
        
        db.session.add(meal)
        db.session.commit()
        
        return meal, 201


class MealResource(Resource):
    
    @marshal_with(meal_detail_schema)
    def get(self, meal_id):
        meal = Meal.query.get_or_404(meal_id)
        return meal, 200
    
    @marshal_with(meal_detail_schema)
    def put(self, meal_id):
        """Update a meal."""
        meal = Meal.query.get_or_404(meal_id)
        
        # Create parser with fields from the meal schema
        parser = reqparse.RequestParser()
        parser.add_argument(
            'name', 
            type=str,
            location=['form', 'json'],
            trim=True,
            store_missing=False
        )
        parser.add_argument(
            'price', 
            type=float,
            location=['form', 'json'],
            store_missing=False
        )
        parser.add_argument(
            'origin_planet', 
            type=str,
            location=['form', 'json'],
            trim=True,
            store_missing=False
        )
        parser.add_argument(
            'description', 
            type=str,
            location=['form', 'json'],
            trim=True,
            store_missing=False
        )
        
        args = parser.parse_args()
        
        # Validate and update fields if provided
        if 'name' in args:
            if len(args['name']) < 2:
                return {'message': 'Meal name must be at least 2 characters'}, 400
            
            if len(args['name']) > 100:
                return {'message': 'Meal name cannot exceed 100 characters'}, 400
                
            meal.name = args['name']
            
        if 'price' in args:
            if args['price'] <= 0:
                return {'message': 'Meal price must be greater than 0'}, 400
                
            meal.price = args['price']
            
        if 'origin_planet' in args:
            if len(args['origin_planet']) < 2:
                return {'message': 'Origin planet must be at least 2 characters'}, 400
                
            if len(args['origin_planet']) > 50:
                return {'message': 'Origin planet cannot exceed 50 characters'}, 400
                
            meal.origin_planet = args['origin_planet']
            
        if 'description' in args:
            meal.description = args['description']
        
        db.session.commit()
        return meal, 200
    
    def delete(self, meal_id):
        meal = Meal.query.get_or_404(meal_id)
        db.session.delete(meal)
        db.session.commit()
        return {'message': f'Meal {meal_id} deleted'}, 204


class MealIngredientsResource(Resource):
    """Resource for managing a specific meal's ingredients."""
    
    @marshal_with({'ingredients': fields.List(fields.Nested(ingredient_schema))})
    def get(self, meal_id):
        """Get all ingredients for a meal."""
        meal = Meal.query.get_or_404(meal_id)
        return {'ingredients': meal.ingredients}, 200
    
    @marshal_with({'ingredients': fields.List(fields.Nested(ingredient_schema))})
    def post(self, meal_id):
        """Add ingredients to a meal."""
        meal = Meal.query.get_or_404(meal_id)
        
        parser = reqparse.RequestParser()
        parser.add_argument(
            'ingredients',
            type=str,
            action='append',
            required=True,
            help='At least one ingredient is required',
            location=['form', 'json']
        )
        
        args = parser.parse_args()
        
        # Validate ingredients
        if not args['ingredients']:
            return {'message': 'At least one ingredient must be provided'}, 400
            
        for ingredient_name in args['ingredients']:
            if not ingredient_name or len(ingredient_name.strip()) < 2:
                return {'message': 'Ingredient names must be at least 2 characters'}, 400
                
            if len(ingredient_name) > 50:
                return {'message': 'Ingredient names cannot exceed 50 characters'}, 400
        
        # Add new ingredients
        for ingredient_name in args['ingredients']:
            # Standardize ingredient name
            ingredient_name = ingredient_name.strip()
            
            # Check if meal already has this ingredient
            existing_ingredient_names = [i.name for i in meal.ingredients]
            if ingredient_name in existing_ingredient_names:
                continue
                
            # Check if ingredient already exists in the database
            ingredient = Ingredient.query.filter_by(name=ingredient_name).first()
            if not ingredient:
                # Create new ingredient if it doesn't exist
                ingredient = Ingredient(name=ingredient_name)
                db.session.add(ingredient)
            
            # Add the ingredient to the meal
            meal.ingredients.append(ingredient)
        
        db.session.commit()
        return {'ingredients': meal.ingredients}, 200
    
    @marshal_with({'ingredients': fields.List(fields.Nested(ingredient_schema))})
    def delete(self, meal_id):
        """Remove ingredients from a meal."""
        meal = Meal.query.get_or_404(meal_id)
        
        parser = reqparse.RequestParser()
        parser.add_argument(
            'ingredients',
            type=str,
            action='append',
            required=True,
            help='At least one ingredient is required',
            location=['form', 'json']
        )
        
        args = parser.parse_args()
        
        # Validate ingredients
        if not args['ingredients']:
            return {'message': 'At least one ingredient must be provided'}, 400
        
        # Remove specified ingredients
        for ingredient_name in args['ingredients']:
            # Standardize ingredient name
            ingredient_name = ingredient_name.strip()
            
            ingredient = Ingredient.query.filter_by(name=ingredient_name).first()
            if ingredient and ingredient in meal.ingredients:
                meal.ingredients.remove(ingredient)
        
        db.session.commit()
        return {'ingredients': meal.ingredients}, 200