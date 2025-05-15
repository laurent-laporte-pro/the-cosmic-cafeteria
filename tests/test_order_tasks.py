import pytest
from unittest.mock import patch, MagicMock
from worker.tasks import process_order_task


@pytest.mark.parametrize("sleep_time", [1, 2, 3, 4, 5])
@patch("worker.tasks.time.sleep", autospec=True)
@patch("worker.tasks.process_order_logic", autospec=True)
@patch("worker.tasks.logger")
def test_process_order_task_success(mock_logger, mock_process_logic, mock_sleep, sleep_time):
    mock_sleep.return_value = None
    mock_process_logic.return_value = "COMPLETED"

    # Patch random.uniform to return controlled sleep_time
    with patch("worker.tasks.random.uniform", return_value=sleep_time):
        process_order_task(123)

    # Assert sleep was called with the mocked sleep_time
    mock_sleep.assert_called_once_with(sleep_time)

    # Assert process_order_logic called with any session and correct order_id
    mock_process_logic.assert_called_once()
    args = mock_process_logic.call_args[0]
    assert args[1] == 123  # order_id is second positional argument

    # Assert logger info called once
    mock_logger.info.assert_called_once()
    assert "Order 123 processed" in mock_logger.info.call_args[0][0]


@patch("worker.tasks.time.sleep", autospec=True)
@patch("worker.tasks.process_order_logic", side_effect=Exception("Boom"))
@patch("worker.tasks.logger")
def test_process_order_task_failure(mock_logger, mock_process_logic, mock_sleep):
    mock_sleep.return_value = None

    process_order_task(999)

    mock_logger.exception.assert_called_once()
    assert "Failed to process order 999" in mock_logger.exception.call_args[0][0]
