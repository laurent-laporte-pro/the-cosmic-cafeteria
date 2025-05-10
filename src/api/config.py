class Config:
    SQLALCHEMY_DATABASE_URI = "postgresql://user:password@tcc-db:5432/cosmic_cafeteria"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    REDIS_URL = "redis://tcc-redis:6379/0"  # Using Docker service name
    REDIS_HOST = "tcc-redis"
    REDIS_PORT = 6379
    REDIS_DB = 0
