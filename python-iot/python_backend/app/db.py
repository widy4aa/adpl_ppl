import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime
from app.config import DB_CONFIG
import logging

def get_db_connection():
    return psycopg2.connect(**DB_CONFIG)

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
            sensor_data.get('last_update', datetime.now())
        ))
        # print("send data sukses")
        conn.commit()
    except Exception as e:
        logging.error(f"DB error: {e}")
    finally:
        if conn:
            conn.close()
