from api.extensions import ma
from api.models.Meal import Meal

class MealSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Meal
        include_fk = True
        load_instance = True