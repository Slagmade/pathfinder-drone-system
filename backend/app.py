from flask import Flask, jsonify

app = Flask(__name__)

# Dummy data structure for demonstration.
# In your real project, this should be updated by your telemetry/detection logic.
data = {
    "drone1": {
        "position": [ -35.363262, 149.165237 ],
        "detections": [
            {"lat": -35.363, "lon": 149.166, "status": "detected"}
        ],
        "guidance": [
            {"human": [ -35.363, 149.166 ], "safe_zone": [ -35.364, 149.167 ]}
        ]
    },
    "drone2": {
        "position": [ -35.363262, 149.165237 ],
        "detections": [],
        "guidance": []
    }
}

@app.route("/api/data")
def get_data():
    # Returns the latest data as JSON
    return jsonify(data)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)

