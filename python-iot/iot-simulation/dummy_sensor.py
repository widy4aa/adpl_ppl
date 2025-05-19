import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import json
import random
import time
from datetime import datetime

device_status = {
    "fan": "off",
    "water": "off",
    "lamp": "off",
    "mode": "manual"
}

device_id = "Esp-Widya"
BROKER = "broker.emqx.io"
PORT = 1883

# MQTT: Fungsi jika menerima pesan dari Laravel
def on_message(client, userdata, msg):
    global device_status
    try:
        payload = json.loads(msg.payload.decode())
        print("[CONTROL RECEIVED]", payload)

        # Update status jika ada key yang valid
        if "device_status" in payload:
            for key in ["fan", "water", "lamp", "mode"]:
                if key in payload["device_status"] and payload["device_status"][key] in ["on", "off", "auto", "manual"]:
                    device_status[key] = payload["device_status"][key]
            print(f"Updated device status: {device_status}")
            # Publish device info when control changes
            publish_device_info()
    except Exception as e:
        print(f"Failed to process control message: {e}")

# Fungsi untuk publish device info
def publish_device_info():
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    device_info = {
        "device_id": device_id,
        "timestamp": timestamp,
        "device_status": device_status,  # Using the updated device_status
    }
    publish.single("maggot/device/info", json.dumps(device_info), hostname=BROKER, port=PORT)
    print("Published device_info:")
    print(json.dumps(device_info, indent=4))

# MQTT: Setup subscriber untuk kontrol
client = mqtt.Client()
client.on_message = on_message
client.connect(BROKER, PORT)
client.subscribe("maggot/device/control")
client.loop_start()

# Publish device info on startup
publish_device_info()

try:
    while True:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # === Sensor data ===
        sensor_data = {
            "device_id": device_id,
            "timestamp": timestamp,
            "sensor": {
                "suhu_udara": round(random.uniform(20.0, 40.0), 1),
                "kelembapan_udara": random.randint(30, 90),
                "suhu_tanah": round(random.uniform(18.0, 35.0), 1),
                "kelembapan_tanah": random.randint(20, 80)
            }
        }

        # === Timestamp only ===
        timestamp_info = {
            "device_id": device_id,
            "timestamp": timestamp
        }

        # Publish sensor data and timestamp
        publish.single("maggot/sensor/info", json.dumps(sensor_data), hostname=BROKER, port=PORT)
        publish.single("maggot/timestamp", json.dumps(timestamp_info), hostname=BROKER, port=PORT)

        print("Published sensor_data:")
        print(json.dumps(sensor_data, indent=4))
        print("=" * 50)

        time.sleep(2)

except KeyboardInterrupt:
    print("Stopped by user.")
    client.loop_stop()
    client.disconnect()
