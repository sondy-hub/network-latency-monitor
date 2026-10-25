# 此測試會在MySQL中寫入一個假的資料，請注意

from datetime import datetime, timedelta

from anomaly_detector import AnomalyTracker
from database import (
    get_connection,
    save_anomaly_start,
    save_anomaly_recovery
)

ping_results = [25, None, None, None, None, 30]

base_time = datetime(2026, 10, 15, 21, 0, 0)

tracker = AnomalyTracker()
active_anomaly_id = None

connection = get_connection()

try:
    for i, ping in enumerate(ping_results):

        timestamp = base_time + timedelta(seconds=2 * i)

        event = tracker.process_ping(ping, timestamp)

        if event is not None:

            if event["type"] == "anomaly_started":
                active_anomaly_id = save_anomaly_start(connection, event["start_time"])

            elif event["type"] == "anomaly_recovered":
                save_anomaly_recovery(connection, active_anomaly_id, event["recovery_time"], event["duration_seconds"])
                active_anomaly_id = None

finally:
    connection.close()