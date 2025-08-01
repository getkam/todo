from flask import Flask, render_template, request, redirect
from pymongo import MongoClient

import os

app = Flask(__name__)

MONGO_URI = os.environ.get("MONGO_URI", "mongodb://localhost:27017")
client = MongoClient(MONGO_URI)
db = client["todo_db"]
todos = db["todos"]

@app.route("/", methods=["GET"])
def index():
    items = list(todos.find())
    return render_template("index.html", todos=items)


@app.route("/add", methods=["POST"])
def add():
    task = request.form.get("task")
    if task:
        todos.insert_one({"task": task, "done": False})
    return redirect("/")


@app.route("/complete/<item_id>", methods=["POST"])
def complete(item_id):
    from bson.objectid import ObjectId
    todos.update_one({"_id": ObjectId(item_id)}, {"$set": {"done": True}})
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
