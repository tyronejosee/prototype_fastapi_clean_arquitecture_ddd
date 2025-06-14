from sqlalchemy.orm import Session

from app.domain.entities.product import Product
from app.application.schemas.product import (
    ProductCreateSchema,
    ProductUpdateSchema,
)


class ProductRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_all(self, skip: int = 0, limit: int = 100) -> list[Product]:
        return self.db.query(Product).offset(skip).limit(limit).all()

    def get_by_id(self, product_id: int) -> Product | None:
        return self.db.query(Product).filter(Product.id == product_id).first()

    def create(self, product_create: ProductCreateSchema) -> Product:
        product = Product(**product_create.model_dump())
        self.db.add(product)
        self.db.commit()
        self.db.refresh(product)
        return product

    def update(
        self,
        product: Product,
        product_update: ProductUpdateSchema,
    ) -> Product:
        update_data = product_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(product, field, value)

        self.db.commit()
        self.db.refresh(product)
        return product

    def delete(self, product: Product) -> None:
        self.db.delete(product)
        self.db.commit()

    def search_by_name(self, name: str) -> list[Product]:
        return (
            self.db.query(Product)
            .filter(
                Product.name.ilike(f"%{name}%"),
            )
            .all()
        )

    def get_by_category(self, category: str) -> list[Product]:
        return (
            self.db.query(Product)
            .filter(
                Product.category == category,
            )
            .all()
        )
