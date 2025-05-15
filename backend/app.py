from flask import Flask, jsonify, request
from flask_cors import CORS
from audio_service import AudioSystem
from rescue_relay import send_to_rescue_team
from datetime import datetime
import asyncio
from mavsdk import System

app = Flask(__name__)
CORS(app)

# Global data store
victims = []
audio = AudioSystem()

# Telemetry monitoring (simplified)
async def monitor_drone(port, drone_id):
    drone = System()
    await drone.connect(f"udp://127.0.0.1:{port}")
    
    async for position in drone.telemetry.position():
        pass  # Actual implementation would update positions

# Routes
@app.route("/api/data")
def get_data():
    return jsonify({
        "drone1": {"position": [-35.363262, 149.165237]},
        "drone2": {"position": [-35.363262, 149.165237]}
    })

@app.route("/api/victims", methods=["POST"])
def add_victim():
    data = request.json
    victims.append({
        "id": len(victims)+1,
        "lat": data['lat'],
        "lon": data['lon'],
        "timestamp": datetime.now().isoformat()
    })
    return jsonify({"status": "Victim added", "count": len(victims)})

@app.route("/api/victims")
def list_victims():
    return jsonify(victims)

@app.route("/api/alert", methods=["POST"])
def broadcast_alert():
    message = request.json.get("message", "")
    audio.play_message(message)
    return jsonify({"status": "Alert broadcasted"})

@app.route("/api/relay", methods=["POST"])
def relay_data():
    victim_id = request.json.get('victim_id')
    victim = next((v for v in victims if v['id'] == victim_id), None)
    
    if not victim or not send_to_rescue_team(victim):
        return jsonify({"error": "Relay failed"}), 500
    return jsonify({"status": "Data relayed to rescue team"})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)

