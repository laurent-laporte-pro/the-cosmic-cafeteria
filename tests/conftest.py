import pytest
from datetime import datetime
from redis import Redis
from rq import Queue
from api.app import create_app
from api.extensions import db as _db
from api.models import Hero, Meal, Order, OrderStatus

# ---- Core Application Fixtures ----
@pytest.fixture(scope='session')
def app():
    """Create and configure a new app instance for tests."""
    app = create_app()
    app.config.update({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'postgresql://user:password@localhost:5432/test_db',
        'REDIS_URL': 'redis://localhost:6379/1',
        'WTF_CSRF_ENABLED': False
    })
    
    # Establish application context
    with app.app_context():
        yield app

@pytest.fixture(scope='session')
def db(app):
    """Session-wide test database."""
    _db.create_all()
    yield _db
    _db.drop_all()
    _db.session.remove()

@pytest.fixture
def client(app):
    """Test client for the API."""
    return app.test_client()

# ---- Redis/Queue Fixtures ----
@pytest.fixture
def redis_conn(app):
    """Redis connection fixture."""
    conn = Redis.from_url(app.config['REDIS_URL'])
    conn.flushdb()  # Clean before each test
    yield conn
    conn.flushdb()

@pytest.fixture
def test_queue(redis_conn):
    """RQ queue fixture."""
    q = Queue(connection=redis_conn)
    yield q
    q.empty()

