import os


class Config:
    #SQLALCHEMY_DATABASE_URI = "postgresql://user:password@localhost:5832/cosmic_cafeteria"
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
