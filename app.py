from flask import Flask, request
from pymongo import MongoClient
from datetime import datetime

app = Flask(_name_)

client = MongoClient("mongodb://localhost:27017/")
db = client["webhook_db"]
collection = db["webhook_events"]

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    data["timestamp"] = datetime.utcnow().isoformat()
    collection.insert_one(data)
    return {"message": "Webhook received"}, 200

@app.route("/get-events", methods=["GET"])
def get_events():
    events = list(collection.find().sort("timestamp", -1))
    for e in events:
        e["_id"] = str(e["_id"])
    return events

if _name_ == "_main_":
    app.run(port=5000)