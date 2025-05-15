from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields, validate
from api.models.meal import Meal
from api.app_extensions import db

class MealSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Meal
        load_instance = True
        sqla_session = db.session

    name = fields.Str(
        required=True,
        validate=validate.Length(min=1, max=100),
        error_messages={"required": "Name is required."}
    )
    ingredients = fields.List(
        fields.Str(validate=validate.Length(min=1)),
        required=True,
        validate=validate.Length(min=1),  # At least one ingredient
        error_messages={"required": "Ingredients are required."}
    )
    price = fields.Float(
        required=True,
        validate=validate.Range(min=0.01, error="Price must be greater than zero."),
        error_messages={"required": "Price is required."}
    )
    origin_planet = fields.Str(
        required=True,
        validate=validate.Length(min=1, max=100),
        error_messages={"required": "Origin planet is required."}
    )
    description = fields.Str(
        required=False,
        validate=validate.Length(max=500),
        allow_none=True
    )
