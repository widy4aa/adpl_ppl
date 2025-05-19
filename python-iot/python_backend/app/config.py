import logging

DB_CONFIG = {
    "dbname": "maggot",
    "user": "postgres",
    "password": "dio",
    "host": "localhost", 
    "port": "5432"
}

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%d-%m-%Y %H:%M:%S',
    handlers=[logging.StreamHandler()]
)
