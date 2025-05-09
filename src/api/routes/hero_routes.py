"""
Hero routes for the Cosmic Cafeteria API.

This module demonstrates how to use Flask-RESTful schemas for request parsing and response marshalling.
"""
from flask import request
from flask_restful import Resource, marshal_with, reqparse, fields, inputs

from ..models import Hero, Allergy, db
from ..schemas import hero_schema, hero_create_schema, hero_detail_schema, hero_allergy_update_schema, allergy_schema


class HeroListResource(Resource):
    
    @marshal_with(hero_schema)
    def get(self):
        """Get all heroes."""
        heroes = Hero.query.all()
        return heroes, 200
    
    @marshal_with(hero_schema)
    def post(self):
        parser = reqparse.RequestParser()
        # Add validation for name and planet
        parser.add_argument(
            'name', 
            type=str,
            required=True,
            help='Name is required',
            location=['form', 'json'],
            # Add validation for name (non-empty, max length)
            trim=True,
            nullable=False
        )
        parser.add_argument(
            'planet', 
            type=str,
            required=True,
            help='Planet is required',
            location=['form', 'json'],
            # Add validation for planet (non-empty)
            trim=True,
            nullable=False
        )
        
        args = parser.parse_args()
        
        # Additional validation
        if len(args['name']) < 2:
            return {'message': 'Hero name must be at least 2 characters'}, 400
            
        if len(args['name']) > 50:
            return {'message': 'Hero name cannot exceed 50 characters'}, 400
        
        if len(args['planet']) < 2:
            return {'message': 'Planet name must be at least 2 characters'}, 400
        
        if len(args['planet']) > 50:
            return {'message': 'Planet name cannot exceed 50 characters'}, 400
        
        # Create hero
        hero = Hero(name=args['name'], planet=args['planet'])
        db.session.add(hero)
        db.session.commit()
        
        return hero, 201


class HeroResource(Resource):
    
    @marshal_with(hero_detail_schema)
    def get(self, hero_id):
        hero = Hero.query.get_or_404(hero_id)
        return hero, 200
    
    @marshal_with(hero_detail_schema)
    def put(self, hero_id):
        """Update a hero."""
        hero = Hero.query.get_or_404(hero_id)
        
        parser = reqparse.RequestParser()
        parser.add_argument(
            'name', 
            type=str,
            location=['form', 'json'],
            trim=True,
            store_missing=False
        )
        parser.add_argument(
            'planet', 
            type=str,
            location=['form', 'json'],
            trim=True,
            store_missing=False
        )
        
        args = parser.parse_args()
        
        # Validate input if provided
        if 'name' in args:
            if args['name'] is None or len(args['name']) < 2:
                return {'message': 'Hero name must be at least 2 characters'}, 400
                
            if len(args['name']) > 50:
                return {'message': 'Hero name cannot exceed 50 characters'}, 400
            
            hero.name = args['name']
            
        if 'planet' in args:
            if args['planet'] is None or len(args['planet']) < 2:
                return {'message': 'Planet name must be at least 2 characters'}, 400
            
            if len(args['planet']) > 50:
                return {'message': 'Planet name cannot exceed 50 characters'}, 400
                
            hero.planet = args['planet']
        
        db.session.commit()
        return hero, 200
    
    def delete(self, hero_id):
        hero = Hero.query.get_or_404(hero_id)
        db.session.delete(hero)
        db.session.commit()
        return {'message': f'Hero {hero_id} deleted'}, 204


class HeroAllergiesResource(Resource):
    
    @marshal_with({'allergies': fields.List(fields.Nested(allergy_schema))})
    def get(self, hero_id):
        """Get all allergies for a hero."""
        hero = Hero.query.get_or_404(hero_id)
        return {'allergies': hero.allergies}, 200
    
    @marshal_with({'allergies': fields.List(fields.Nested(allergy_schema))})
    def post(self, hero_id):
        """Add allergies to a hero."""
        hero = Hero.query.get_or_404(hero_id)
        
        parser = reqparse.RequestParser()
        parser.add_argument(
            'allergies',
            type=str,
            action='append',
            required=True,
            help='At least one allergy is required',
            location=['form', 'json']
        )
        
        args = parser.parse_args()
        
        # Validate allergies
        if not args['allergies']:
            return {'message': 'At least one allergy must be provided'}, 400
            
        for allergy_name in args['allergies']:
            if not allergy_name or len(allergy_name.strip()) < 2:
                return {'message': 'Allergy names must be at least 2 characters'}, 400
                
            if len(allergy_name) > 50:
                return {'message': 'Allergy names cannot exceed 50 characters'}, 400
        
        # Add new allergies
        for allergy_name in args['allergies']:
            # Standardize allergy names (trim and lowercase)
            allergy_name = allergy_name.strip()
            
            # Check if hero already has this allergy
            existing_allergy_names = [a.name for a in hero.allergies]
            if allergy_name in existing_allergy_names:
                continue
                
            # Check if allergy already exists in the database
            allergy = Allergy.query.filter_by(name=allergy_name).first()
            if not allergy:
                # Create new allergy if it doesn't exist
                allergy = Allergy(name=allergy_name)
                db.session.add(allergy)
            
            # Add the allergy to the hero
            hero.allergies.append(allergy)
        
        db.session.commit()
        return {'allergies': hero.allergies}, 200
    
    @marshal_with({'allergies': fields.List(fields.Nested(allergy_schema))})
    def delete(self, hero_id):
        """Remove allergies from a hero."""
        hero = Hero.query.get_or_404(hero_id)
        
        parser = reqparse.RequestParser()
        parser.add_argument(
            'allergies',
            type=str,
            action='append',
            required=True,
            help='At least one allergy is required',
            location=['form', 'json']
        )
        
        args = parser.parse_args()
        
        # Validate allergies
        if not args['allergies']:
            return {'message': 'At least one allergy must be provided'}, 400
        
        # Remove specified allergies
        for allergy_name in args['allergies']:
            # Standardize allergy name
            allergy_name = allergy_name.strip()
            
            allergy = Allergy.query.filter_by(name=allergy_name).first()
            if allergy and allergy in hero.allergies:
                hero.allergies.remove(allergy)
        
        db.session.commit()
        return {'allergies': hero.allergies}, 200