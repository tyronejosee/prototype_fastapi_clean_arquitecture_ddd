# Prototype FastAPI Ecommerce

A comprehensive clothing ecommerce API built with FastAPI, following Clean Architecture and Domain-Driven Design (DDD) principles, [Example architecture](./arquitecture.md).

<!-- TODO: Add image and video -->
<!-- [Main](.main.webp) -->
<!-- [Youtube video](https://youtu.be/dQw4w9WgXcQ) -->

## ✨ Features

* **Authentication**: JWT-based authentication with access and refresh tokens
* **User Management**: User registration, login, and profile management
* **Product Management**: Complete CRUD operations for products with search and filtering
* **Shopping Cart**: Add, update, remove items from cart
* **Order Management**: Checkout process with order creation and payment simulation
* **Payment Processing**: Mock payment processor for testing and development
* **Role-Based Access**: Admin-only endpoints for product management
* **Testing**: Comprehensive test suite with pytest and HTTPX

## 🏗️ Architecture

The project follows Clean Architecture principles with the following structure:

```bash
app/
# TODO: Add folder structure
```

## 💾 Installation

Requirements:

* [Python](https://www.python.org/) 3.10 or higher
* [uv](https://docs.astral.sh/uv/guides/install-python/)

Create a virtual environment:

```bash
uv venv .venv
```

Activate the virtual environment:

```bash
# Linux/macOS
source .venv/bin/activate

# Windows
.venv\Scripts\activate
```

Install dependencies:

```bash
uv pip install -r requirements.txt
```

Set up environment variables:

```bash
cp .env.example .env
# Edit .env with your configuration
```

Initialize the database:

```bash
alembic upgrade head
```

Run the application:

```bash
uvicorn app.main:app --reload
```

## 🧪 Testing

Run the test suite:

```bash
pytest
```

Run tests with coverage:

```bash
pytest --cov=app
```

## 🧑‍💻 Development

### Database Migrations

Create a new migration:

```bash
alembic revision --autogenerate -m "Description of changes"
```

Apply migrations:

```bash
alembic upgrade head
```

## 🔧 Environment Variables

* `DATABASE_URL`: Database connection string
* `SECRET_KEY`: JWT secret key
* `ALGORITHM`: JWT algorithm (default: HS256)
* `ACCESS_TOKEN_EXPIRE_MINUTES`: Access token expiration (default: 30)
* `REFRESH_TOKEN_EXPIRE_DAYS`: Refresh token expiration (default: 7)
* `DEBUG`: Debug mode (default: True)

## 🚀 Production Deployment

1. Set up PostgreSQL database
2. Configure environment variables
3. Run database migrations
4. Use a production WSGI server like Gunicorn:

```bash
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker
```

## 🔐 Security Features

* Password hashing with bcrypt
* JWT tokens with expiration
* Role-based access control
* Input validation with Pydantic
* SQL injection prevention with SQLAlchemy ORM
* CORS configuration for cross-origin requests

## ⚖️ License

This project is licensed under the MIT License.
