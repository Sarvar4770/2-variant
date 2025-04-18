
from flask import Flask, request, jsonify

app = Flask(__name__)
users = {}

@app.route("/api/register", methods=["POST"])
def register():
    data = request.json
    name = data.get("name")
    phone = data.get("phone")
    tg_id = data.get("telegram_id")

    if not all([name, phone, tg_id]):
        return jsonify({"error": "Missing fields"}), 400

    if tg_id not in users:
        user_id = f"A{len(users)+1:02d}"
        users[tg_id] = {"name": name, "phone": phone, "id": user_id, "locations": {}}
    return jsonify({"userId": users[tg_id]["id"]})

@app.route("/api/location", methods=["POST"])
def save_location():
    data = request.json
    tg_id = data.get("telegram_id")
    lat = data.get("lat")
    lon = data.get("lon")
    label = data.get("label")

    if not all([tg_id, lat, lon, label]):
        return jsonify({"error": "Missing data"}), 400

    if tg_id not in users:
        return jsonify({"error": "User not found"}), 404

    loc_id = f"{users[tg_id]['id']}_{label.upper()}"
    users[tg_id]["locations"][label] = {"lat": lat, "lon": lon, "id": loc_id}

    return jsonify({"locationId": loc_id})

@app.route("/api/find/<loc_id>")
def find_location(loc_id):
    for user in users.values():
        for label, loc in user.get("locations", {}).items():
            if loc["id"] == loc_id:
                return jsonify({"lat": loc["lat"], "lon": loc["lon"]})
    return jsonify({"error": "ID not found"}), 404
