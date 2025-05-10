from api.extensions import db

class Meal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    ingredients = db.Column(db.ARRAY(db.String), nullable=False)
    price = db.Column(db.Float, nullable=False)
    origin_planet = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500), nullable=True)
    
    ordered_by = db.relationship('Order', backref='meal', lazy=True) #one to many

    def __init__(self, name, ingredients, price, origin_planet, description=None):
        self.name = name
        self.ingredients = ingredients
        self.price = price
        self.origin_planet = origin_planet
        self.description = description
        
    def __repr__(self):
        return self.name
