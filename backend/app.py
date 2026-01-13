from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from flask_cors import CORS
from knowledge_engine import KnowledgeEngine

app = Flask(__name__)  # ✅ Corrected
CORS(app)
ke = KnowledgeEngine()
app.config["MONGO_URI"] = "mongodb://localhost:27017/krishi_sakhi"
mongo = PyMongo(app)

# ✅ Register API (no OTP, sample testing)
@app.route('/register', methods=['POST'])
def register():
    data = request.json
    name = data.get('name')
    mobile = data.get('mobile')
    password = data.get('password')

    if mongo.db.users.find_one({"mobile": mobile}):
        return jsonify({"message": "Already registered"}), 400

    user_id = mongo.db.users.insert_one({
        "name": name,
        "mobile": mobile,
        "password": password
    }).inserted_id

    return jsonify({"message": "Registration successful", "user_id": str(user_id)}), 201

# ✅ Login API
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    mobile = data.get('mobile')
    password = data.get('password')

    user = mongo.db.users.find_one({"mobile": mobile, "password": password})
    if user:
        return jsonify({"message": "Login successful", "name": user["name"]})
    else:
        return jsonify({"message": "Invalid mobile or password"}), 401

@app.route("/recommend", methods=["POST"])
def recommend():
    data = request.get_json()
    crop = data.get("crop")
    soil = data.get("soil")
    temp = data.get("temp")
    humidity = data.get("humidity")
    lang = data.get("lang", "en")  # pass "ml" for Malayalam

    rec = ke.recommend(crop, soil, temp, humidity, lang=lang)
    return jsonify(rec)

# ✅ Use double underscores here as well
if __name__ == "__main__":
    app.run(debug=True)
