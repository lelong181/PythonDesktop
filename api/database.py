import mysql.connector
from config.database_config import DB_CONFIG

def get_connection():
    return mysql.connector.connect(**DB_CONFIG) 