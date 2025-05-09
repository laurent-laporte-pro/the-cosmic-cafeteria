"""
Utility functions for The Cosmic Cafeteria API.

This module contains helper functions used throughout the API.
"""
from datetime import datetime
from typing import Dict, List, Optional, Union
import re

from .models import Meal, Order, Hero


def format_date(date_obj: datetime, format_str: str = "%Y-%m-%d") -> str:
    """Format a datetime object as a string."""
    if not date_obj:
        return ""
    
    return date_obj.strftime(format_str)


def validate_planet_name(planet_name: str) -> bool:
    """Validate that a planet name follows the established naming conventions."""
    if not planet_name:
        return False
    

    if len(planet_name) < 3:
        return False
    

    if not planet_name[0].isupper():
        return False
    

    if not re.match(r'^[A-Za-z0-9 -]+$', planet_name):
        return False
    
    return True


def calculate_order_total(meal_id: int, quantity: int) -> float:
    """Calculate the total price for an order."""
    meal = Meal.query.get(meal_id)
    if not meal:
        raise ValueError(f"Meal with ID {meal_id} not found")
    
    return meal.price * quantity


def group_orders_by_planet(orders: List[Order]) -> Dict[str, List[Order]]:
    """Group orders by the planet of the hero who placed them."""
    result = {}
    
    for order in orders:
        hero = order.hero
        if not hero:
            continue
        
        planet = hero.planet
        if planet not in result:
            result[planet] = []
        
        result[planet].append(order)
    
    return result


def check_for_allergies(hero_id: int, meal_id: int) -> Optional[List[str]]:
    """Check if a hero is allergic to any ingredient in a meal."""
    hero = Hero.query.get(hero_id)
    meal = Meal.query.get(meal_id)
    
    if not hero or not meal:
        return None
    
    hero_allergies = {allergy.name.lower() for allergy in hero.allergies}
    meal_ingredients = {ingredient.name.lower() for ingredient in meal.ingredients}
    
    allergic_ingredients = hero_allergies.intersection(meal_ingredients)
    
    return list(allergic_ingredients) if allergic_ingredients else None