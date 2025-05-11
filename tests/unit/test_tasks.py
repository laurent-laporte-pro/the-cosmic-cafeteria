import pytest
from unittest.mock import patch, MagicMock, call
from datetime import datetime
from src.api.models import Order, OrderStatus, Hero, Meal
from src.worker.tasks import process_order, handle_failed_order

# ---- Test Data Fixtures ----
@pytest.fixture
def mock_order():
    order = MagicMock(spec=Order)
    order.id = 1
    order.status = OrderStatus.PENDING
    order.hero = MagicMock(spec=Hero)
    order.meal = MagicMock(spec=Meal)
    order.processed_at = None
    return order

@pytest.fixture
def mock_db_session():
    with patch('worker.tasks.db.session') as mock:
        yield mock

# ---- Success  Tests ----
def test_process_order_success(mock_order, mock_db_session):
    """Test successful order processing"""
    # Setup
    mock_order.hero.allergies = []
    mock_order.meal.ingredients = ["safe_ingredient"]
    
    with patch('worker.tasks.Order.query.get', return_value=mock_order), \
         patch('worker.tasks.time.sleep') as mock_sleep:
        
        # Execute
        process_order(mock_order.id)
        
        # Verify
        assert mock_order.status == OrderStatus.COMPLETED
        assert mock_order.processed_at is not None
        mock_db_session.commit.assert_called()
        mock_sleep.assert_called_once()

# ---- Failed test ----
def test_process_order_allergy_rejection(mock_order, mock_db_session):
    """Test order rejection due to allergies"""
    # Setup
    mock_order.hero.allergies = ["peanuts"]
    mock_order.meal.ingredients = ["peanuts", "salt"]
    
    with patch('worker.tasks.Order.query.get', return_value=mock_order):
        # Execute
        process_order(mock_order.id)
        
        # Verify
        assert mock_order.status == OrderStatus.CANCELLED
        assert "peanuts" in mock_order.message
        mock_db_session.commit.assert_called()
