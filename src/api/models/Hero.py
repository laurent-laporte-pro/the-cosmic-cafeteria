from api.extensions import db

class Hero(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    planet = db.Column(db.String(100), nullable=False)
    allergies = db.Column(db.ARRAY(db.String), default=[])
    
    orders = db.relationship('Order', backref='hero', lazy=True)

    def __init__(self, name, planet, allergies):
        self.name = name
        self.planet = planet
        self.allergies = allergies
        
    def __repr__(self):
        return self.name
