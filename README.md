
# Velox 0.1

[![Python Version](https://img.shields.io/badge/python-3.10+-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

**Velox** is a lightweight, modern Python web framework with a built-in ORM for SQLite.  
It is designed for clean, maintainable code and rapid API development.

---

## 🚀 Key Features

- **Fast Routing:** Decorator-based routes supporting multiple HTTP methods.
- **Built-in ORM:** Minimal SQLite ORM for table creation, insertion, and querying.
- **JSON Requests & Responses:** Automatic parsing and response formatting.
- **Command-Line Utility:** Manage database without running the server.
- **Lightweight & Extendable:** Minimal boilerplate, fully Python standard library.
- **Multiple Methods per Path:** GET, POST, PUT, etc., on same endpoint.

---

## 📦 Installation

Clone the repository:

```bash
git clone https://github.com/maroofiums/velox.git
cd velox
````

No external dependencies required.
Python 3.10+ recommended.

---

## 🛠 Usage

### 1️⃣ Running the Server

```bash
python miniapi.py
```

Open in browser or use curl:

```
GET http://localhost:8000/users
POST http://localhost:8000/users
```

---

### 2️⃣ CLI Commands (ORM Utility)

Velox CLI allows database management **without starting the server**.

#### Create Table

```bash
python miniapi.py create_table users id:INTEGER name:TEXT email:TEXT
```

#### Insert Record

```bash
python miniapi.py insert users name=Ali email=ali@test.com
```

#### Fetch Records

```bash
python miniapi.py fetch users
```

---

### 3️⃣ Example API Routes

```python
@api.route("/users", methods=["GET"])
def get_users(request, db):
    return {"users": db.fetch_all("users")}

@api.route("/users", methods=["POST"])
def create_user(request, db):
    return db.insert("users", request.body)
```

---

## 🔮 Roadmap

* Support **path parameters** `/users/<id>`
* Add **PUT & DELETE methods**
* Middleware: Logging, Authentication
* Modular framework structure (multi-file)
* Async database and HTTP support

---

## 💡 Why Velox?

Velox is ideal for:

* Developers learning frameworks or APIs
* Rapid prototyping of small projects
* Lightweight alternatives to DRF or FastAPI
* CLI-driven database management

---

## 📚 Documentation

* Core ORM: `Database` class (`create_table`, `insert`, `fetch_all`)
* Core API: `MiniAPI` class (`route`, `run`)
* Request / Response: `Request` object and `Response.json()`

---
