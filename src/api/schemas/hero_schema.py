from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields, validate
from api.models.hero import Hero
from api.app_extensions import db


class HeroSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Hero
        load_instance = True           
        ordered = True                
        sqla_session = db.session 

    name = fields.Str(
        required=True,
        validate=validate.Length(min=1, max=100),
        error_messages={"required": "Name is required."}
    )

    planet = fields.Str(
        required=True,
        validate=validate.Length(min=1, max=100),
        error_messages={"required": "Planet is required."}
    )

    allergies = fields.List(
        fields.Str(validate=validate.Length(min=1, max=100)),
        load_default=list
    )
