from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.domain.entities.product import Product
from app.interfaces.api.dependencies import get_current_admin_user
from app.infrastructure.repositories.product_repository import (
    ProductRepository,
)
from app.application.schemas.product import (
    ProductSchema,
    ProductCreateSchema,
    ProductUpdateSchema,
)

router = APIRouter()


@router.get("/", response_model=list[ProductSchema])
async def get_products(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    category: Optional[str] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db),
) -> list[Product]:
    product_repo = ProductRepository(db)

    if search:
        return product_repo.search_by_name(search)
    elif category:
        return product_repo.get_by_category(category)
    else:
        return product_repo.get_all(skip=skip, limit=limit)


@router.get("/{product_id}", response_model=ProductSchema)
async def get_product(
    product_id: int,
    db: Session = Depends(get_db),
) -> Product:
    product_repo = ProductRepository(db)
    product = product_repo.get_by_id(product_id)

    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
        )

    return product


@router.post(
    "/",
    response_model=ProductSchema,
    status_code=status.HTTP_201_CREATED,
)
async def create_product(
    product_create: ProductCreateSchema,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_admin_user),
) -> Product:
    product_repo = ProductRepository(db)
    return product_repo.create(product_create)


@router.put("/{product_id}", response_model=ProductSchema)
async def update_product(
    product_id: int,
    product_update: ProductUpdateSchema,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_admin_user),
) -> Product:
    product_repo = ProductRepository(db)
    product = product_repo.get_by_id(product_id)

    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
        )

    return product_repo.update(product, product_update)


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_admin_user),
) -> None:
    product_repo = ProductRepository(db)
    product = product_repo.get_by_id(product_id)

    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
        )

    product_repo.delete(product)
