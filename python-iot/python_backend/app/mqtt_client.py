import json
from datetime import datetime
import threading
import time
import logging
import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
from app.state import sensor_info, device_info,device_info_control
from app.db import save_sensor_data

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        client.subscribe("maggot/sensor/info")
        client.subscribe("maggot/device/info")
    else:
        logging.error(f"MQTT failed with code {rc}")

def on_message(client, userdata, msg):
    try:
        payload = json.loads(msg.payload.decode())
        current_time = datetime.now().isoformat()

        if msg.topic == "maggot/sensor/info":
            sensor_info.update({
                "last_update": payload.get("timestamp") or current_time,
                **payload.get("sensor", {})
            })
            # print("get data sensor sukses")

        elif msg.topic == "maggot/device/info":
            device_info.update({
                "last_update": payload.get("timestamp") or current_time,
                **payload.get("device_status", {})
            })
            print("get data device sukses : ",device_info)
            print("Mw di ubah jadi ini : ",device_info_control)
    except Exception as e:
        logging.error(f"MQTT message error: {e}")

def start_mqtt_client():
    client = mqtt.Client(client_id="maggot-monitor-server")
    client.on_connect = on_connect
    client.on_message = on_message
    try:
        client.connect("broker.emqx.io", 1883, 60)
        client.loop_forever()
    except Exception as e:
        logging.error(f"MQTT connection error: {e}")

def publish_device_info(device_info_control: dict):
    try:
        payload = {
            "device_id": "Esp-Widya",
            "timestamp": datetime.now().isoformat(),
            "device_status": {
                "fan": device_info_control.get("fan"),
                "water": device_info_control.get("water"),
                "lamp": device_info_control.get("lamp"),
                "mode": device_info_control.get("mode"),
            },
        }

        publish.single(
            topic="maggot/device/control",
            payload=json.dumps(payload),
            hostname="broker.emqx.io",
            port=1883
        )

        logging.info(f"Published device_info to MQTT: {payload}")
    except Exception as e:
        logging.error(f"MQTT publish error: {e}")
        
def save_data_periodically():
    while True:
        time.sleep(10)
        if sensor_info.get("last_update"):
            save_sensor_data(1, sensor_info)


