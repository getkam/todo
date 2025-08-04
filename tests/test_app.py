import pytest
from app import app, todos
from bson.objectid import ObjectId

@pytest.fixture
def client():
    app.config["TESTING"] = True
    test_client = app.test_client()

    # Wyczyść bazę danych przed każdym testem
    todos.delete_many({})
    yield test_client
    todos.delete_many({})  # również po

def test_add_task(client):
    response = client.post("/add", data={"task": "Zadanie testowe"})
    assert response.status_code == 302  # redirect
    assert todos.count_documents({}) == 1

def test_index_page(client):
    todos.insert_one({"task": "Zadanie A", "done": False})
    response = client.get("/")
    assert response.status_code == 200
    assert b"Zadanie A" in response.data

def test_complete_task(client):
    task = {"task": "Do zrobienia", "done": False}
    inserted = todos.insert_one(task)
    task_id = str(inserted.inserted_id)

    response = client.post(f"/complete/{task_id}")
    assert response.status_code == 302  # redirect

    updated = todos.find_one({"_id": ObjectId(task_id)})
    assert updated["done"] is True
