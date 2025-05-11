# COSMIC CAFETERIA API DOCUMENTATION (Abdelatif Aitouche)

# INTRO 
---

##  Project Structure & Design

To ensure clean architecture and maintainability:

- **Modular Design**: Each model is defined in its own file to promote separation of concerns and scalability.
- **Blueprints**: Flask Blueprints are used to split routes by functionality (e.g., heroes, meals, orders).
- **Serialization**: Utilizes **Marshmallow** for data validation, serialization, and deserialization.
- **App Factory Pattern**: The app is initialized using a `create_app()` factory function for flexibility across environments.
- **Extensions**: Database and Marshmallow instances are initialized in `extensions.py` to avoid circular imports and duplicate instantiation.
- **Configuration**: DB credentials and Redis config are stored in a centralized `config.py` file.
- **Logging**: Python's built-in `logging` module is used to log application activity for transparency and debugging.

---

##  Testing

- All API routes were tested using **Postman**.
- Unit and integration tests are written and organized in the `tests/` folder.

---

##  Environment

- The project runs inside a **Python virtual environment**.
- For simplicity, a `.env` file was not used. However, `python-dotenv` can be easily integrated for environment-based configuration in production.


##  Running the Project

docker-compose up --build





## ENDPOINTS
     - BASE_URL/heroes/
     - BASE_URL/meals/
     - BASE_URL/orders/
     - BASE_URL/heroes/<int:id>
     - BASE_URL/meals/<int:id>
     - BASE_URL/orders/<int:id>
     - BASE_URL/orders/<hero_id , meal_id>
     - BASE_URL/orders/<str:status>






## Heroes Management

GET /heroes/
Description: List all registered heroes
Response:

json
    [
        {
            "name": "Iron Man",
            "planet" : "ExoPlanet",
            "allergies": ["metal"],
        }
    ]

POST /heroes/
Description: Register a new hero
Request Body:

json
    {
        "name": "Hulk",
        "allergies": ["Skill issue"]
    }

Success Response:
json
    {
        "id": 2,
        "name": "Hulk",
    }

GET /heroes/<int:id>
Description: Get hero details
Response:

json
    {
        "id": 1,
        "name": "Iron Man",
        "allergies": ["Skill issue"],
    }


## Meals Management
GET /meals/
Description: List all available meals

Response:

json
[
  {
    "id": 1,
    "name": "Vibranium Burger",
    "ingredients": ["Skill issue", "Kryptonite"],
  }
]


POST /meals/
Description: Add new meal
Request Body:

json
{
  "name": "Pym Particle Soup",
  "ingredients": ["pym particles", "herbs"]
}


## Orders Management
POST /orders/
Description: Create new order
Request Body:

json
{
  "hero_id": 1,
  "meal_id": 3,
}

Response (202 Accepted):

json
{
  "order_id": 5,
  "status": "PENDING",
  "message": "Order received for processing",
}

GET /orders/<int:id>
Description: Check order status
Response:

json
{
  "id": 5,
  "status": "COMPLETED",
  "hero": "Iron Man",
  "meal": "Vibranium Burger",
  "order_time": "2023-07-25T12:05:00Z",
  "completed_time": order_time + 5secs
}


GET /orders/<str:status>
Description: Filter orders by status
Allowed Statuses: PENDING, PROCESSING, COMPLETED, REJECTED
Example: GET /orders/COMPLETED
Response:

json
[
  {
    "id": 3,
    "hero": "Thor",
    "meal": "Asgardian Feast",
    "completed_at": "2023-07-25T11:30:00Z"
  }
]



EXAMPLES
Create Order Flow


# 1. Create hero
curl -X POST BASE_URL/heroes \
  -d '{"name":"Black Panther", "planet" : "terre" , "allergies":["vibranium"]}'

# 2. Create meal 
curl -X POST BASE_URL/meals \
  -d '{"name":"Wakandan Feast","ingredients":["vibranium","herbs"]}'

# 3. Place order
curl -X POST BASE_URL/orders \
  -d '{"hero_id":1,"meal_id":1}'