import pytest
from app import app, todos
from bson.objectid import ObjectId

@pytest.fixture
def client():
    app.config["TESTING"] = True
    test_client = app.test_client()

    # Deleteing database before testing
    todos.delete_many({})
    yield test_client
    todos.delete_many({})  # deleteing database after testing

def test_add_task(client):
    response = client.post("/add", data={"task": "New task"})
    assert response.status_code == 302  # redirect
    assert todos.count_documents({}) == 1

def test_index_page(client):
    todos.insert_one({"task": "Task A", "done": False})
    response = client.get("/")
    assert response.status_code == 200
    assert b"Task A" in response.data

def test_complete_task(client):
    task = {"task": "Task B", "done": False}
    inserted = todos.insert_one(task)
    task_id = str(inserted.inserted_id)

    response = client.post(f"/complete/{task_id}")
    assert response.status_code == 302  # redirect

    updated = todos.find_one({"_id": ObjectId(task_id)})
    assert updated["done"] is True
