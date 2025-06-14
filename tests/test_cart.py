from fastapi.testclient import TestClient


def test_get_empty_cart(client: TestClient, auth_headers):
    response = client.get("/api/v1/cart/", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["items"] == []
    assert data["total_price"] == 0
    assert data["total_items"] == 0


def test_add_to_cart(client: TestClient, test_product, auth_headers):
    cart_item_data = {"product_id": test_product.id, "quantity": 2}
    response = client.post(
        "/api/v1/cart/items", json=cart_item_data, headers=auth_headers
    )
    assert response.status_code == 201
    data = response.json()
    assert data["product_id"] == test_product.id
    assert data["quantity"] == 2


def test_add_to_cart_insufficient_stock(client: TestClient, test_product, auth_headers):
    cart_item_data = {
        "product_id": test_product.id,
        "quantity": 15,  # More than available stock (10)
    }
    response = client.post(
        "/api/v1/cart/items", json=cart_item_data, headers=auth_headers
    )
    assert response.status_code == 400
    assert "Insufficient stock" in response.json()["detail"]


def test_get_cart_with_items(client: TestClient, test_product, auth_headers):
    # Add item to cart
    cart_item_data = {"product_id": test_product.id, "quantity": 2}
    client.post("/api/v1/cart/items", json=cart_item_data, headers=auth_headers)

    # Get cart
    response = client.get("/api/v1/cart/", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) == 1
    assert data["total_items"] == 2
    assert data["total_price"] == test_product.price * 2


def test_update_cart_item(client: TestClient, test_product, auth_headers):
    # Add item to cart
    cart_item_data = {"product_id": test_product.id, "quantity": 2}
    client.post("/api/v1/cart/items", json=cart_item_data, headers=auth_headers)

    # Update quantity
    update_data = {"quantity": 3}
    response = client.put(
        f"/api/v1/cart/items/{test_product.id}", json=update_data, headers=auth_headers
    )
    assert response.status_code == 200
    data = response.json()
    assert data["quantity"] == 3


def test_remove_cart_item(client: TestClient, test_product, auth_headers):
    # Add item to cart
    cart_item_data = {"product_id": test_product.id, "quantity": 2}
    client.post("/api/v1/cart/items", json=cart_item_data, headers=auth_headers)

    # Remove item
    response = client.delete(
        f"/api/v1/cart/items/{test_product.id}", headers=auth_headers
    )
    assert response.status_code == 204

    # Verify cart is empty
    cart_response = client.get("/api/v1/cart/", headers=auth_headers)
    assert len(cart_response.json()["items"]) == 0


def test_clear_cart(client: TestClient, test_product, auth_headers):
    # Add item to cart
    cart_item_data = {"product_id": test_product.id, "quantity": 2}
    client.post("/api/v1/cart/items", json=cart_item_data, headers=auth_headers)

    # Clear cart
    response = client.delete("/api/v1/cart/", headers=auth_headers)
    assert response.status_code == 204

    # Verify cart is empty
    cart_response = client.get("/api/v1/cart/", headers=auth_headers)
    assert len(cart_response.json()["items"]) == 0
