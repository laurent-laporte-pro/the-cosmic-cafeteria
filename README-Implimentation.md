
# 🚀 Flask RESTful User API

This is a simple Flask REST API using:

- `Flask >= 3.1.0`
- `Flask-RESTful >= 0.3.10`
- `Flask-SQLAlchemy >= 3.1.1`
- `Click` for CLI commands


---

## 🚧 Setup Instructions

### 1. 🔧 Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. 🛠️ Set Environment Variable

```bash
export FLASK_APP=run.py
export FLASK_ENV=development
```

Or on Windows:

```cmd
set FLASK_APP=run.py
set FLASK_ENV=development
```

### 3. 🧱 Initialize the Database

```bash
flask create-db
```

---

## 🚀 Running the App

```bash
python run.py
```

Visit: [http://127.0.0.1:5000/users](http://127.0.0.1:5000/users)

---

## 📬 API Endpoints

### `GET /users`

Returns a list of all users.

**Example response:**
```json
[
  {
    "id": 1,
    "username": "john"
  }
]
```

---

### `POST /users`

Creates a new user.

**Request body:**
```sh
curl -X POST http://127.0.0.1:5000/users \
     -H "Content-Type: application/json" \
     -d '{"username": "john"}'

```

**Response:**
```json
{
  "id": 1,
  "username": "john"
}
```

---

## 🧪 Testing with `curl`

```bash
curl -X POST http://127.0.0.1:5000/users      -H "Content-Type: application/json"      -d '{"username": "john"}'
```

---

## 📌 Notes

- Database is SQLite (`db.sqlite3`) by default.
- You can add more models, routes, and CLI commands as needed.
