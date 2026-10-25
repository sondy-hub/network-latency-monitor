import os
from dotenv import load_dotenv

load_dotenv()

PING_TARGET = os.getenv("PING_TARGET", "8.8.8.8")

HIGH_LATENCY_THRESHOLD = int(os.getenv("HIGH_LATENCY_THRESHOLD", "70"))

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = int(os.getenv("DB_PORT", "3306"))
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME", "network_monitor")