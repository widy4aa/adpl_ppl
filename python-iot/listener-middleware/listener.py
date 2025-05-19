import json
from flask import Flask, jsonify, request
import threading
import paho.mqtt.client as mqtt
from datetime import datetime
import logging
import psycopg2
import time
from psycopg2.extras import RealDictCursor


#var--------------------------------------------------------------------------------
DB_CONFIG = {
    "dbname": "maggot",
    "user": "postgres",
    "password": "dio",
    "host": "localhost", 
    "port": "5432"
}

sensor_info = {
    "last_update": None,    
    "suhu_tanah":None,
    "suhu_udara":None,
    "kelembapan_tanah":None,
    "kelembapan_udara":None
};

device_info = {
   "last_update": None,    
    "fan":None,
    "water":None,
    "lamp":None,
    "mode":None
}

#conf--------------------------------------------------------------------------------
def get_db_connection():
    return psycopg2.connect(**DB_CONFIG)

latest_data_lock = threading.Lock()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%d-%m-%Y %H:%M:%S',
    handlers=[
        logging.StreamHandler()
    ]
)


#API-----------------------------------------------------------------------------------

app = Flask(__name__)

@app.route("/api/sensor/info", methods=["GET"])
def get_latest_sensor_data():
    response = {
        "data": {
            "device_id": "Esp-Widya",
            "last_update": sensor_info["last_update"],
            "suhu_tanah" : sensor_info["suhu_tanah"],
            "suhu_udara" : sensor_info["suhu_udara"],
            "kelembapan_tanah" : sensor_info['kelembapan_tanah'],
            "kelembapan_udara" : sensor_info['kelembapan_udara']

        }
    }
    return jsonify(response)

@app.route("/api/device/info", methods=["GET"])
def get_latest_device_data():
    response = {
        "data": {
            "device_id": "Esp-Widya",
            "last_update": device_info["last_update"],
            "fan" : device_info["fan"],
            "water" : device_info["water"],
            "lamp" : device_info['lamp'],
            "mode" : device_info['mode']

        }
    }
    return jsonify(response)

@app.route("/api/device/health", methods=["GET"])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "Maggot Monitoring API"
    })


#mqttt get-----------------------------------------------------------------------------------

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        client.subscribe("maggot/sensor/info")
        client.subscribe("maggot/device/info")
    else:
        logging.error(f"Connection failed {rc}")

def on_message(client, userdata, msg):
    global latest_data
    try:
        payload = json.loads(msg.payload.decode())
        current_time = datetime.now().isoformat()

        
        if msg.topic == "maggot/sensor/info":
            sensor_info["last_update"] = payload.get("timestamp") or current_time
            sensor_data = payload.get("sensor", {})  # Get the nested sensor object or empty dict if not exists
            sensor_info.update({
                "suhu_tanah": sensor_data.get("suhu_tanah"),
                "suhu_udara": sensor_data.get("suhu_udara"),
                "kelembapan_tanah": sensor_data.get("kelembapan_tanah"),
                "kelembapan_udara": sensor_data.get("kelembapan_udara")
            })

            print("Updated sensor info:", sensor_info)

        elif msg.topic == "maggot/device/info":
            # Handle device info format
            device_info["last_update"] = payload.get("timestamp") or current_time
            device_data = payload.get("device_status",{})
            device_info["fan"] = device_data.get("fan")
            device_info["water"] = device_data.get("water")
            device_info["lamp"] = device_data.get("lamp")
            device_info["mode"] = device_data.get("mode")
            
            print("Updated device info:", device_info)
            pass
        else:
            logging.warning(f"Unexpected topic: {msg.topic}")
            
    except Exception as e:
        logging.error(f"Error processing {msg.topic}: {e}")

def start_mqtt_client():
    client = mqtt.Client(client_id="maggot-monitor-server")
    client.on_connect = on_connect
    client.on_message = on_message
    
    try:
        client.connect("broker.emqx.io", 1883, 60)
        logging.info("Starting MQTT client loop")
        client.loop_forever()
    except Exception as e:
        logging.error(f"MQTT connection error: {e}")

#Database----------------------------------------------------------------------------------------------------------------------------

def save_sensor_data(device_id, sensor_data):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO sensor_logs 
            (id_device, kelembapan_udara, kelembapan_tanah, suhu_udara, suhu_tanah, recorded_at)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            device_id,
            sensor_data.get('kelembapan_udara'),
            sensor_data.get('kelembapan_tanah'),
            sensor_data.get('suhu_udara'),
            sensor_data.get('suhu_tanah'),
            sensor_data.get('last_update', datetime.now())  # Use payload timestamp or current time
        ))

        conn.commit()
        logging.info(f"Successfully saved data for device {device_id}")
    except Exception as e:
        logging.error(f"Failed to save data to DB: {e}")
    finally:
        if conn:
            conn.close()

def save_data_periodically():
    while True:
        time.sleep(10)
        
        # Check if sensor_info has data
        if sensor_info.get('last_update'):  # Only proceed if we have data
            save_sensor_data(
                device_id=1,
                sensor_data={
                    'kelembapan_udara': sensor_info.get('kelembapan_udara'),
                    'kelembapan_tanah': sensor_info.get('kelembapan_tanah'),
                    'suhu_udara': sensor_info.get('suhu_udara'),
                    'suhu_tanah': sensor_info.get('suhu_tanah'),
                    'last_update': sensor_info.get('last_update')
                }
            )
            logging.info("Data inserted successfully")

#Runtime-------------------------------------------------------------------------------

if __name__ == "__main__":

    
    mqtt_thread = threading.Thread(target=start_mqtt_client, name="MQTT-Thread")
    mqtt_thread.daemon = True
    mqtt_thread.start()

    background_saver = threading.Thread(target=save_data_periodically, name="DB-Saver")
    background_saver.daemon = True
    background_saver.start()
    
    logging.info("Starting Flask API server on port 5000")
    app.run(host='0.0.0.0', port=5000, debug=False)  