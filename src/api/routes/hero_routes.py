from flask import Blueprint, request , jsonify
from api.extensions import db

from api.models.Hero import Hero
from api.schemas.hero_schema import HeroSchema


hero_blueprint = Blueprint("hero_blueprint" , __name__ , url_prefix="/heros")
hero_schema = HeroSchema()
heros_schema = HeroSchema(many = True)



@hero_blueprint.route('/' , methods = ['GET'])
def get_heros():
    heros = Hero.query.all()
    return heros_schema.jsonify(heros)



@hero_blueprint.route('/' , methods = ['POST'])
def create_hero():
    data = request.get_json()
    hero = hero_schema.load(data)
    db.session.add(hero)
    db.session.commit()
    return hero_schema.jsonify(hero) , 201