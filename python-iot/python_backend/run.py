from app.api import app
from app.mqtt_client import start_mqtt_client, save_data_periodically
import threading
import logging

if __name__ == "__main__":
    threading.Thread(target=start_mqtt_client, daemon=True).start()
    threading.Thread(target=save_data_periodically, daemon=True).start()

    logging.info("Running Flask server on port 5000")
    app.run(host="0.0.0.0", port=5000)
