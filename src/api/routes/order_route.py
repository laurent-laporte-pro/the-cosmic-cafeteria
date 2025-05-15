from flask import Blueprint
from api.views.order_view import OrderAPI

order_bp = Blueprint('order', __name__)

order_view = OrderAPI.as_view('order_api')
order_bp.add_url_rule('/orders/', defaults={'order_id': None}, view_func=order_view, methods=['GET'])
order_bp.add_url_rule('/orders/', view_func=order_view, methods=['POST'])
order_bp.add_url_rule('/orders/<int:order_id>', view_func=order_view, methods=['GET', 'DELETE'])
