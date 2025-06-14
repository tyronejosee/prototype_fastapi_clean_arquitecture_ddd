from fastapi.testclient import TestClient

from app.domain.entities.product import Product


def test_get_products(client: TestClient, test_product: Product) -> None:
    response = client.get("/api/v1/products/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == "Test T-Shirt"


def test_get_product_by_id(client: TestClient, test_product: Product) -> None:
    response = client.get(f"/api/v1/products/{test_product.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test T-Shirt"
    assert data["price"] == 29.99


def test_get_nonexistent_product(client: TestClient) -> None:
    response = client.get("/api/v1/products/999")
    assert response.status_code == 404


def test_create_product_admin(
    client: TestClient,
    admin_auth_headers: dict,
) -> None:
    product_data = {
        "name": "New Jacket",
        "description": "A warm jacket",
        "price": 89.99,
        "stock": 5,
        "category": "outerwear",
    }
    response = client.post(
        "/api/v1/products/", json=product_data, headers=admin_auth_headers
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "New Jacket"
    assert data["price"] == 89.99


def test_create_product_non_admin(
    client: TestClient,
    auth_headers: dict,
) -> None:
    product_data = {
        "name": "New Jacket",
        "description": "A warm jacket",
        "price": 89.99,
        "stock": 5,
        "category": "outerwear",
    }
    response = client.post(
        "/api/v1/products/",
        json=product_data,
        headers=auth_headers,
    )
    assert response.status_code == 403


def test_update_product(client: TestClient, test_product, admin_auth_headers):
    update_data = {"price": 39.99, "stock": 15}
    response = client.put(
        f"/api/v1/products/{test_product.id}",
        json=update_data,
        headers=admin_auth_headers,
    )
    assert response.status_code == 200
    data = response.json()
    assert data["price"] == 39.99
    assert data["stock"] == 15


def test_delete_product(client: TestClient, test_product, admin_auth_headers):
    response = client.delete(
        f"/api/v1/products/{test_product.id}", headers=admin_auth_headers
    )
    assert response.status_code == 204

    # Verify product is deleted
    get_response = client.get(f"/api/v1/products/{test_product.id}")
    assert get_response.status_code == 404


def test_search_products(client: TestClient, test_product):
    response = client.get("/api/v1/products/?search=shirt")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert "shirt" in data[0]["name"].lower()


def test_filter_products_by_category(client: TestClient, test_product):
    response = client.get("/api/v1/products/?category=clothing")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["category"] == "clothing"
