from fastapi.testclient import TestClient

from app.domain.entities.product import Product


def test_checkout_success(client: TestClient, test_product, auth_headers):
    # Add item to cart
    cart_item_data = {"product_id": test_product.id, "quantity": 2}
    client.post(
        "/api/v1/cart/items",
        json=cart_item_data,
        headers=auth_headers,
    )

    # Checkout
    order_data = {"payment_method": "credit_card"}
    response = client.post(
        "/api/v1/orders/checkout", json=order_data, headers=auth_headers
    )
    assert response.status_code == 201
    data = response.json()
    assert data["status"] == "confirmed"
    assert data["total_price"] == test_product.price * 2
    assert len(data["order_items"]) == 1


def test_checkout_empty_cart(client: TestClient, auth_headers):
    order_data = {"payment_method": "credit_card"}
    response = client.post(
        "/api/v1/orders/checkout", json=order_data, headers=auth_headers
    )
    assert response.status_code == 400
    assert "Cart is empty" in response.json()["detail"]


def test_get_user_orders(
    client: TestClient,
    test_product,
    auth_headers,
) -> None:
    # Add item to cart and checkout
    cart_item_data = {"product_id": test_product.id, "quantity": 1}
    client.post("/api/v1/cart/items", json=cart_item_data, headers=auth_headers)

    order_data = {"payment_method": "credit_card"}
    checkout_response = client.post(
        "/api/v1/orders/checkout", json=order_data, headers=auth_headers
    )
    order_id = checkout_response.json()["id"]

    # Get orders
    response = client.get("/api/v1/orders/", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["id"] == order_id


def test_get_order_by_id(
    client: TestClient,
    test_product: Product,
    auth_headers: dict,
) -> None:
    # Add item to cart and checkout
    cart_item_data = {"product_id": test_product.id, "quantity": 1}
    client.post(
        "/api/v1/cart/items",
        json=cart_item_data,
        headers=auth_headers,
    )

    order_data = {"payment_method": "credit_card"}
    checkout_response = client.post(
        "/api/v1/orders/checkout", json=order_data, headers=auth_headers
    )
    order_id = checkout_response.json()["id"]

    # Get specific order
    response = client.get(f"/api/v1/orders/{order_id}", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == order_id
    assert len(data["order_items"]) == 1


def test_get_nonexistent_order(client: TestClient, auth_headers: dict) -> None:
    response = client.get("/api/v1/orders/999", headers=auth_headers)
    assert response.status_code == 404
