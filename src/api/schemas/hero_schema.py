from api.extensions import ma
from api.models.Hero import Hero
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema


class HeroSchema(ma.SQLAlchemyAutoSchema):
    class Meta : 
        model = Hero
        load_instance = True