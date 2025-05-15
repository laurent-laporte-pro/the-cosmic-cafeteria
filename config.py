import os
import logging
from pathlib import Path
from typing import List, Optional
import logging
from logging.config import dictConfig

basedir = Path(__file__).parent.parent.resolve()


def parse_list(env_var: Optional[str], delimiter: str = ",") -> List[str]:
    """
    Parse a delimited string from an environment variabl into a list of strings.

    This is useful for handling environment variables like:
    ALLOWED_HOSTS="localhost,127.0.0.1,example.com"
    """
    if not env_var:
        return []
    return [item.strip() for item in env_var.split(delimiter) if item.strip()]


class Config:
    """
    Base configuration class. Use environment variables for sensitive info.
    """

    SECRET_KEY: str = os.getenv("SECRET_KEY", "super-secret-key")
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False

    DEBUG: bool = False
    TESTING: bool = False

    ALLOWED_HOSTS: List[str] = parse_list(os.getenv("ALLOWED_HOSTS"))

    SQLALCHEMY_DATABASE_URI: str = os.getenv(
        "DATABASE_URI", f"sqlite:///{basedir / 'app.db'}"
    )

    WTF_CSRF_ENABLED: bool = True  # Enable by default

    REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

    log_dir = 'logs'
    os.makedirs(log_dir, exist_ok=True)

    LOG_LEVEL = logging.INFO
    LOG_FILE = 'logs/app.log'

    @staticmethod
    def init_log_app(app):
        dictConfig({
            'version': 1,
            'disable_existing_loggers': False,
            'formatters': {
                'default': {
                    'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
                },
            },
            'handlers': {
                'console': {
                    'class': 'logging.StreamHandler',
                    'formatter': 'default',
                    'level': Config.LOG_LEVEL,
                },
                'file': {
                    'class': 'logging.handlers.RotatingFileHandler',
                    'filename': Config.LOG_FILE,
                    'maxBytes': 1_000_000,
                    'backupCount': 5,
                    'formatter': 'default',
                    'level': Config.LOG_LEVEL,
                },
            },
            'root': {
                'level': Config.LOG_LEVEL,
                'handlers': ['console', 'file']
            },
        })




class DevelopmentConfig(Config):
    DEBUG: bool = True
    SQLALCHEMY_DATABASE_URI: str = os.getenv(
        "DEV_DATABASE_URI", f"sqlite:///{basedir / 'dev.db'}"
    )


class TestingConfig(Config):
    """
    Config for running tests with Pytest.
    Uses in-memory SQLite DB and disables CSRF.
    """
    TESTING: bool = True
    DEBUG: bool = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:" 
    WTF_CSRF_ENABLED: bool = False


class ProductionConfig(Config):
    #should be implemened
    pass 


config_map = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
}



def get_config(env: Optional[str] = None) -> Config:
    env = env or os.getenv("FLASK_ENV", "development")
    config_class = config_map.get(env, DevelopmentConfig)
    return config_class()
