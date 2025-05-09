from flask_restful import fields


class OrderStatusField(fields.Raw):
    def format(self, value):
        if value is None:
            return None
        return value.value


hero_schema = {
    'id': fields.Integer,
    'name': fields.String,
    'planet': fields.String,
}

hero_create_schema = {
    'name': fields.String,
    'planet': fields.String,
}


allergy_schema = {
    'name': fields.String(attribute='name'),
}


hero_allergy_update_schema = {
    'allergies': fields.List(fields.String),
}

ingredient_schema = {
    'name': fields.String(attribute='name'),
}


meal_ingredient_update_schema = {
    'ingredients': fields.List(fields.String),
}

meal_schema = {
    'id': fields.Integer,
    'name': fields.String,
    'price': fields.Float,
    'origin_planet': fields.String,
    'description': fields.String,
}

meal_create_schema = {
    'name': fields.String,
    'price': fields.Float,
    'origin_planet': fields.String,
    'description': fields.String,
}


order_status_schema = OrderStatusField()

order_schema = {
    'id': fields.Integer,
    'status': order_status_schema,
    'message': fields.String,
    'order_time': fields.DateTime,
    'completed_time': fields.DateTime,
    'hero_id': fields.Integer,
    'meal_id': fields.Integer,
    'hero': fields.Nested(hero_schema),
    'meal': fields.Nested(meal_schema),
}




hero_detail_schema = {
    **hero_schema,
    'allergies': fields.List(fields.Nested(allergy_schema)),
    'orders': fields.List(fields.Nested({
        'id': fields.Integer,
        'status': order_status_schema,
        'order_time': fields.DateTime,
    })),
}

meal_detail_schema = {
    **meal_schema,
    'ingredients': fields.List(fields.Nested(ingredient_schema)),
    'ordered_by': fields.List(fields.Nested({
        'id': fields.Integer,
        'hero_id': fields.Integer,
        'hero': fields.Nested(hero_schema),
    })),
}

__all__ = [
    "hero_schema", 
    "hero_create_schema",
    "allergy_schema",
    "hero_allergy_update_schema",
    "ingredient_schema",
    "meal_ingredient_update_schema",
    "meal_schema", 
    "meal_create_schema",
    "order_schema", 
    "order_create_schema",
    "order_status_schema",
    "hero_detail_schema",
    "meal_detail_schema",
]
