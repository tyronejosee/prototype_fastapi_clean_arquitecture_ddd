from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.database import create_tables
from app.interfaces.api.v1.routes import (
    auth,
    users,
    products,
    cart,
    orders,
)

# Create tables
create_tables()

app = FastAPI(
    title="Prototype FastAPI Ecommerce",
    description="A prototype FastAPI ecommerce application",
    version="1.0.0",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(
    auth.router,
    prefix="/api/v1/auth",
    tags=["Authentication"],
)
app.include_router(
    users.router,
    prefix="/api/v1/users",
    tags=["Users"],
)
app.include_router(
    products.router,
    prefix="/api/v1/products",
    tags=["Products"],
)
app.include_router(
    cart.router,
    prefix="/api/v1/cart",
    tags=["Cart"],
)
app.include_router(
    orders.router,
    prefix="/api/v1/orders",
    tags=["Orders"],
)


@app.get("/")
async def root() -> dict:
    return {"message": "Welcome to Prototype FastAPI Ecommerce!"}


@app.get("/health")
async def health_check() -> dict:
    return {"status": "healthy"}
