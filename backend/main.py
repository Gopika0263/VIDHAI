from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
import asyncio
from datetime import datetime, timedelta

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# MongoDB setup
client = MongoClient("mongodb://localhost:27017/")
db = client["agrisens"]
notifications_col = db["notifications"]

# Connected websockets
clients = []

# WebSocket endpoint
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    clients.append(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            # frontend can send messages if needed
    except WebSocketDisconnect:
        clients.remove(websocket)

# Function to send notification to all connected clients
async def send_notification_to_clients(notification):
    for client in clients:
        await client.send_json(notification)

# Background task: generate reminder every 60 seconds
async def notification_generator():
    while True:
        # Example reminder data
        notification = {
            "title": "Crop Reminder",
            "message": "Water your wheat field!",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        notifications_col.insert_one(notification)  # save to DB
        await send_notification_to_clients(notification)
        await asyncio.sleep(60)  # every 60s

# Start background task
@app.on_event("startup")
async def startup_event():
    asyncio.create_task(notification_generator())

# API to get past notifications
@app.get("/notifications")
async def get_notifications():
    notifs = list(notifications_col.find().sort("_id", -1).limit(20))
    for n in notifs:
        n["_id"] = str(n["_id"])
    return notifs
