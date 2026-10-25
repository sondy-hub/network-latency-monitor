import subprocess
import time
from datetime import datetime
import os
import mysql.connector
from database import get_connection
from anomaly_detector import AnomalyTracker
from database import save_anomaly_start, save_anomaly_recovery
from anomaly_detector import HighLatencyTracker
from database import save_high_latency_start, save_high_latency_recovery
from config import PING_TARGET, HIGH_LATENCY_THRESHOLD



# 將ping存入資料庫
def save_ping(connection, time_now, ping):
    cursor = connection.cursor()

    sql = """
    INSERT INTO `ping_records` (`timestamp`, `latency_ms`)
    VALUES (%s, %s)
    """

    values = (time_now, ping)

    cursor.execute(sql,values)
    connection.commit()

    cursor.close()



# 取得ping
def get_ping(ip):
    result = subprocess.run(
        ["ping", ip, "-n", "1"],
        capture_output=True,            # 將執行結果收集起來
        text = True,                    # 將收集到的輸出解碼成字串 str
        timeout = 5
    )

    ping = None

    lines = result.stdout.splitlines()

    for line in lines:
        if "時間=" in line:
            # split()
            ping = int(line.split("時間=")[1].split("ms")[0])
            return ping
    return None


# 取得全部歷史紀錄的統計(ping值成功率)
def get_ping_stats(connection):
    cursor = connection.cursor(dictionary = True)

    sql = """
    SELECT
        COUNT(*) AS total_count,
        COUNT(latency_ms) AS success_count,
        COUNT(*)-COUNT(latency_ms) AS failure_count,
        COUNT(latency_ms) * 100.0 / NULLIF(COUNT(*), 0) AS success_rate,
        (COUNT(*)-COUNT(latency_ms)) * 100.0/ NULLIF(COUNT(*), 0) AS failure_rate
    FROM ping_records;
    """

    cursor.execute(sql)

    result = cursor.fetchone()      # fetchone()：一次取得下一筆。

    cursor.close()

    return result

# 取得最近 N 筆 Ping 紀錄
def get_recent_records(connection, limit: int = 10):
    cursor = connection.cursor(dictionary = True)

    sql = """
    SELECT *
    FROM `ping_records`
    ORDER BY `id` DESC
    LIMIT %s;
    """

    cursor.execute(sql,(limit,))

    result = cursor.fetchall()

    cursor.close()

    return result


# 取得最近 N 小時的統計結果
def get_hourly_stats(connection, hours = 1):
    cursor = connection.cursor(dictionary = True)

    sql = """
    SELECT 
        count(*) AS `total_count`,
        count(`latency_ms`) AS `success_count`,
        AVG(`latency_ms`) AS `average_latency_ms`,
        MAX(`latency_ms`) AS `max_latency_ms`
    FROM `ping_records`
    WHERE `timestamp` >= NOW() - INTERVAL %s HOUR;
    """

    cursor.execute(sql, (hours,))
    result = cursor.fetchone()
    cursor.close()

    return result


if __name__ == "__main__":
    connection = get_connection()

    tracker = AnomalyTracker()
    active_anomaly_id = None

    high_latency_tracker = HighLatencyTracker(threshold=HIGH_LATENCY_THRESHOLD)
    active_high_latency_id = None

    try:
        while True:
            ping = get_ping(PING_TARGET)
            time_now = datetime.now()

            save_ping(connection, time_now, ping)

            if ping is None:
                print(f"{time_now:%Y-%m-%d %H:%M:%S} | 沒有取得 Ping 數值")

            else:
                print(f"{time_now:%Y-%m-%d %H:%M:%S} | Ping 延遲：{ping} ms")


            event = tracker.process_ping(ping, time_now)

            if event is not None:
                if event["type"] == "anomaly_started":
                    active_anomaly_id = save_anomaly_start(connection, event["start_time"])

                elif event["type"] == "anomaly_recovered":
                    save_anomaly_recovery(connection, active_anomaly_id, event["recovery_time"], event["duration_seconds"])
                    active_anomaly_id = None


            high_latency_event = high_latency_tracker.process_ping(ping, time_now)

            if high_latency_event is not None:
                if high_latency_event["type"] == "high_latency_started":
                    active_high_latency_id = save_high_latency_start(connection, high_latency_event["start_time"], high_latency_event["peak_latency_ms"], threshold_ms=high_latency_tracker.threshold)

                elif high_latency_event["type"] == "high_latency_recovered":
                    save_high_latency_recovery(connection, active_high_latency_id, high_latency_event["recovery_time"], high_latency_event["duration_seconds"], high_latency_event["peak_latency_ms"])
                    active_high_latency_id = None

            time.sleep(2)

    except KeyboardInterrupt:
        print("監控已停止")

    finally:
        connection.close()