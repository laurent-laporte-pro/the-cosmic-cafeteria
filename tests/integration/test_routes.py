import pytest
from src.api.models import Hero, Meal, Order, OrderStatus

# ---- Fixtures ----
@pytest.fixture
def sample_hero(db):
    hero = Hero(name="Test Hero", allergies=[])
    db.session.add(hero)
    db.session.commit()
    return hero

@pytest.fixture
def sample_meal(db):
    meal = Meal(name="Test Meal", ingredients=[])
    db.session.add(meal)
    db.session.commit()
    return meal

@pytest.fixture
def sample_order(db, sample_hero, sample_meal):
    order = Order(hero=sample_hero, meal=sample_meal)
    db.session.add(order)
    db.session.commit()
    return order

# ---- Hero Routes ----
def test_create_hero(client, db):
    response = client.post('/heroes', json={
        "name": "New Hero",
        "allergies": ["kryptonite"]
    })
    assert response.status_code == 201
    assert Hero.query.count() == 1
    assert "kryptonite" in Hero.query.first().allergies

def test_get_hero(client, sample_hero):
    response = client.get(f'/heroes/{sample_hero.id}')
    assert response.status_code == 200
    assert response.json["name"] == "Test Hero"

# ---- Meal Routes ----
def test_create_meal(client, db):
    response = client.post('/meals', json={
        "name": "Cosmic Burger",
        "ingredients": ["space beef", "cosmic bun"]
    })
    assert response.status_code == 201
    assert Meal.query.first().name == "Cosmic Burger"

# ---- Order Routes ----
def test_create_order(client, db, sample_hero, sample_meal):
    response = client.post('/orders', json={
        "hero_id": sample_hero.id,
        "meal_id": sample_meal.id
    })
    assert response.status_code == 202
    assert Order.query.count() == 1
    assert "processing" in response.json["message"]

def test_get_order_status(client, sample_order):
    response = client.get(f'/orders/{sample_order.id}')
    assert response.status_code == 200
    assert response.json["status"] == "PENDING"

def test_update_order_status(client, db, sample_order):
    response = client.patch(f'/orders/{sample_order.id}', json={
        "status": "PROCESSING"
    })
    assert response.status_code == 200
    assert Order.query.get(sample_order.id).status == OrderStatus.PROCESSING

def test_delete_order(client, db, sample_order):
    response = client.delete(f'/orders/{sample_order.id}')
    assert response.status_code == 204
    assert Order.query.count() == 0

# ---- Error Handling ----
def test_create_order_invalid_data(client):
    response = client.post('/orders', json={
        "hero_id": "invalid",
        "meal_id": 1
    })
    assert response.status_code == 400
    assert "error" in response.json

def test_nonexistent_order(client):
    response = client.get('/orders/9999')
    assert response.status_code == 404



# ---- Full Workflow Test ----
def test_complete_order_workflow(client, db):
    # Create Hero
    hero_res = client.post('/heroes', json={"name": "Workflow Hero"})
    hero_id = hero_res.json["id"]
    
    # Create Meal
    meal_res = client.post('/meals', json={
        "name": "Workflow Meal",
        "ingredients": ["test_ingredient"]
    })
    meal_id = meal_res.json["id"]
    
    # Create Order
    order_res = client.post('/orders', json={
        "hero_id": hero_id,
        "meal_id": meal_id
    })
    order_id = order_res.json["id"]
    
    # Simulate Worker Processing
    order = Order.query.get(order_id)
    order.status = OrderStatus.COMPLETED
    db.session.commit()
    
    # Verify Final Status
    status_res = client.get(f'/orders/{order_id}')
    assert status_res.json["status"] == "COMPLETED"