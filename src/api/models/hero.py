from api.app_extensions import db


class Hero(db.Model):
    __tablename__ = "heroes" 

    id: int = db.Column(db.Integer, primary_key=True)
    name: str = db.Column(db.String(100), nullable=False)
    planet: str = db.Column(db.String(100), nullable=False)
    allergies = db.Column(db.JSON, default=list)


    orders = db.relationship(
        "Order",
        backref="hero",
        passive_deletes=True,
        cascade="all, delete-orphan"
    )

    def __init__(self, name: str, planet: str, allergies: list[str]) -> None:
        self.name = name
        self.planet = planet
        self.allergies = allergies

    def __repr__(self) -> str:
        return f"<Hero id={self.id}, name={self.name}, planet={self.planet}>"
