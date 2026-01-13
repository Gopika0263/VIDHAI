from datetime import datetime
from app import mongo  # import Flask PyMongo instance

def add_notification(title, message):
    """Add notification to MongoDB"""
    mongo.db.notifications.insert_one({
        "title": title,
        "message": message,
        "timestamp": datetime.now()
    })

def get_notifications(limit=50):
    """Get last `limit` notifications"""
    notifs = list(mongo.db.notifications.find().sort("timestamp", -1).limit(limit))
    for n in notifs:
        n["_id"] = str(n["_id"])
    return notifs
