import datetime

from app import db


class Orders(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String)
    item = db.Column(db.String)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
