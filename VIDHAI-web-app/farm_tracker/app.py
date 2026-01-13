from flask import Flask, request, jsonify, render_template
from datetime import datetime
import sqlite3
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # allows frontend JS to call backend

DB = 'farm.db'

def init_db():
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS farm_activities (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            farmer_id TEXT,
            activity_type TEXT,
            crop_name TEXT,
            description TEXT,
            date TEXT,
            created_at TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

def get_db():
    return sqlite3.connect(DB)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/activities', methods=['POST'])
def add_activity():
    data = request.json
    if not data:
        return jsonify({"message": "No data received"}), 400

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO farm_activities (farmer_id, activity_type, crop_name, description, date, created_at)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        data['farmer_id'],
        data['activity_type'],
        data['crop_name'],
        data.get('description', ''),
        data['date'],
        datetime.now().isoformat()
    ))
    conn.commit()
    conn.close()
    return jsonify({"message": "Activity logged successfully"}), 201

@app.route('/activities/<farmer_id>', methods=['GET'])
def get_activities(farmer_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM farm_activities WHERE farmer_id=? ORDER BY date DESC", (farmer_id,))
    rows = cursor.fetchall()
    activities = [{
        "id": r[0],
        "activity_type": r[2],
        "crop_name": r[3],
        "description": r[4],
        "date": r[5]
    } for r in rows]
    conn.close()
    return jsonify(activities)

if __name__ == '__main__':
    app.run(debug=True)