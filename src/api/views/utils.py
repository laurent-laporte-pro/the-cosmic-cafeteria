from flask import jsonify
from typing import Any, Optional


def success_response(data: Any, status: int = 200):
    return jsonify({
        "success": True,
        "data": data,
        "message": None
    }), status


def error_response(message: str, status: int = 400, errors: Optional[Any] = None):
    return jsonify({
        "success": False,
        "message": message,
        "errors": errors
    }), status