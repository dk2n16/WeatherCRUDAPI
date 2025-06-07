import pytest


def test_post_endpoint(client, test_post_update_data):
    response = client.post("/weather/london", json=test_post_update_data)
    assert response.status_code == 201
    data = response.get_json()
    assert data["message"] == "Weather report created"
    assert data["city"] == "london"
    assert data["report"]["city"] == "london"
    assert data["report"]["condition"] == "Sunny"
    assert data["report"]["temperature"] == 20.0


@pytest.mark.parametrize(
    "invalid_data",
    [
        {"city": "oslo", "condition": "Sunny"},  # Missing temperature
        {"city": "oslo", "temperature": 18.0},  # Missing condition
        {"condition": "Sunny", "temperature": 18.0},  # Missing city
        {"city": "oslo", "condition": "Windy", "temperature": 18.0},  # Invalid condition
        {"city": "oslo", "condition": "Sunny", "temperature": "hot"},  # Wrong type for temperature
    ]
)
def test_post_invalid_data(client, invalid_data):
    response = client.post("/weather/oslo", json=invalid_data)
    assert response.status_code == 400
    assert "error" in response.get_json()


def test_get_endpoint(client, populated_db):
    response = client.get("/weather/london")
    assert response.status_code == 200
    data = response.get_json()
    assert data["city"] == "london"
    assert data["report"]["city"] == "london"
    assert data["report"]["condition"] == "Cloudy"
    assert data["report"]["temperature"] == 15.0


def test_get_nonexistent_city(client):
    response = client.get("/weather/timbuktu")
    assert response.status_code == 404
    data = response.get_json()
    assert data["error"] == "City 'timbuktu' not found in the database."


def test_delete_endpoint(client, populated_db):
    response = client.delete("/weather/barcelona")
    assert response.status_code == 200
    data = response.get_json()
    assert data["message"] == "Weather report deleted"
    assert data["city"] == "barcelona"

    # Verify the city is deleted
    response = client.get("/weather/barcelona")
    assert response.status_code == 404
    data = response.get_json()
    assert data["error"] == "City 'barcelona' not found in the database."


def test_delete_nonexistent_city(client):
    response = client.delete("/weather/timbuktu")
    assert response.status_code == 404
    data = response.get_json()
    assert data["error"] == "City 'timbuktu' not found in the database."


def test_update_endpoint(client, populated_db, test_post_update_data):
    get_response = client.get("/weather/london")
    initial_data = get_response.get_json()
    assert initial_data["report"]["temperature"] == 15.0
    response = client.put("/weather/london", json=test_post_update_data)
    assert response.status_code == 200
    data = response.get_json()
    assert data["message"] == "Weather report updated"
    assert data["city"] == "london"
    assert data["report"]["city"] == "london"
    assert data["report"]["condition"] == "Sunny"
    assert data["report"]["temperature"] == 20.0


def test_update_nonexistent_city(client, test_post_update_data):
    test_post_update_data["city"] = "timbuktu"
    response = client.put("/weather/timbuktu", json=test_post_update_data)
    assert response.status_code == 404
    assert "error" in response.get_json()