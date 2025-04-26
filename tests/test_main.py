from fastapi.testclient import TestClient
from main import app
import pytest

client = TestClient(app)

def test_create_program():
    response = client.post(
        "/programs/",
        json={"name": "TB Program", "description": "Tuberculosis treatment program"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "TB Program"
    assert data["description"] == "Tuberculosis treatment program"

def test_list_programs():
    response = client.get("/programs/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_create_client():
    response = client.post(
        "/clients/",
        json={
            "first_name": "John",
            "last_name": "Mwangi",
            "date_of_birth": "1990-01-01",
            "gender": "Male",
            "contact_number": "0712345678",
            "address": "123 Nairobi"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["first_name"] == "John"
    assert data["last_name"] == "Mwangi"

def test_list_clients():
    response = client.get("/clients/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_get_client():
    # First, create a client
    client.post(
        "/clients/",
        json={
            "first_name": "Jane",
            "last_name": "Otieno",
            "date_of_birth": "1990-01-01",
            "gender": "Female",
            "contact_number": "0987654321",
            "address": "456 Nairobi"
        }
    )
    response = client.get("/clients/1")
    assert response.status_code == 200
    data = response.json()
    assert data["first_name"] == "Jane"

def test_enroll_client():
    # First, create a program and a client
    client.post(
        "/programs/",
        json={"name": "HIV Program", "description": "HIV treatment program"}
    )
    client.post(
        "/clients/",
        json={
            "first_name": "Alice",
            "last_name": "Wafula",
            "date_of_birth": "1990-01-01",
            "gender": "Female",
            "contact_number": "1234567890",
            "address": "789 Kakamega"
        }
    )
    response = client.post(
        "/enrollments/",
        json={"client_id": 1, "program_id": 1}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Client enrolled successfully"

def test_search_clients():
    response = client.get("/clients/search/?query=John")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
