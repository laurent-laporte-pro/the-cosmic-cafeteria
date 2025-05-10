import random
import time
from datetime import datetime
from api.extensions import db
from api.models import Order, OrderStatus
from api.app import create_app

def process_order(order_id):
    print('task started processing')
    
    app = create_app()
    with app.app_context():
        order = Order.query.get(order_id)
        if not order:
            return

        try:
            
            order.status = OrderStatus.IN_PROGRESS #update the status to IN PROGRESS
            order.message = "Traitement en cours..."
            db.session.commit()

            
            time.sleep(random.uniform(1, 5)) #RANDOM DELAY

            if set(order.hero.allergies or []) & set(order.meal.ingredients or []): #check for allergies
                order.status = OrderStatus.CANCELLED
                order.message = "Annulé : conflit d'allergies"
            else:
                order.status = OrderStatus.COMPLETED
                order.message = "Commande prête!"

            order.processed_at = datetime.utcnow()
            db.session.commit()

        except Exception as e:
            db.session.rollback()
            order.status = OrderStatus.CANCELLED
            order.message = f"Erreur: {str(e)}"
            db.session.commit()
            raise