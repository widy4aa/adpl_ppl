from flask import Flask, jsonify
from flask import request
from app.state import sensor_info, device_info,device_info_control
from datetime import datetime


from app.state import device_info  # tempat nyimpen state
from app.mqtt_client import publish_device_info  # ini yang kamu buat tadi

app = Flask(__name__)

@app.route("/api/sensor/info", methods=["GET"])
def get_latest_sensor_data():
    return jsonify({"data": {"device_id": "Esp-Widya", **sensor_info}})

@app.route("/api/device/info", methods=["GET"])
def get_latest_device_data():
    return jsonify({"data": {"device_id": "Esp-Widya", **device_info}})


@app.route("/api/device/control", methods=["POST"])
def post_device_status():
    data = request.get_json()

    app.logger.info(f"[POST] Device Status Received: {data}")

    current_time = datetime.now().isoformat()
    device_data = data.get("device_status", {})


    device_info_control.update({
        "last_update": data.get("timestamp", current_time),
        "fan": device_data.get("fan"),
        "lamp": device_data.get("lamp"),
        "water": device_data.get("water"),
        "mode": device_data.get("mode")
    })

    publish_device_info(device_info_control)

    print("var global : ", device_info_control)

    return jsonify({"status": "ok", "received": data}), 200


@app.route("/api/device/health", methods=["GET"])
def health_check():
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "Maggot Monitoring API"
    })
