import mysql.connector
from config import DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME


# 連線建立
def get_connection():
    connection = mysql.connector.connect(
        host = DB_HOST,
        port = DB_PORT,
        user = DB_USER,
        password = DB_PASSWORD,
        database = DB_NAME
    )

    return connection


# 在資料庫中紀錄異常事件
def save_anomaly_start(connection, start_time):
    cursor = connection.cursor()

    sql = """
        INSERT INTO `anomaly_events` (`start_time`)
        VALUES (%s)
    """

    cursor.execute(sql, (start_time,))
    connection.commit()

    anomaly_id = cursor.lastrowid   # 取得透過 INSERT 新增的自動遞增 ID。

    cursor.close()

    return anomaly_id


# 當異常恢復時更新原本的紀錄
def save_anomaly_recovery(connection, anomaly_id, recovery_time, duration_seconds):
    cursor = connection.cursor()

    sql = """
        UPDATE `anomaly_events`
        SET `recovery_time` = %s,
            `duration_seconds` = %s
        WHERE `id` = %s
    """

    cursor.execute(sql,(recovery_time, duration_seconds, anomaly_id))
    
    connection.commit()
    cursor.close()

# 查詢異常事件紀錄
def get_anomaly_events(connection, limit=100):
    cursor = connection.cursor(dictionary=True)

    sql = """
        SELECT * FROM `anomaly_events`
        ORDER BY `id` DESC
        LIMIT %s
    """

    cursor.execute(sql, (limit,))
    result = cursor.fetchall()

    cursor.close()

    return result


# 在資料庫中紀錄高延遲異常事件
def save_high_latency_start(connection, start_time, peak_latency_ms, threshold_ms):
    cursor = connection.cursor()

    sql = """
        INSERT INTO `high_latency_events`(`start_time`, `peak_latency_ms`, `threshold_ms`)
        VALUES(%s, %s, %s)
    """

    cursor.execute(sql, (start_time, peak_latency_ms, threshold_ms))
    connection.commit()

    high_latency_id = cursor.lastrowid
    cursor.close()

    return high_latency_id

# 當高延遲異常恢復時更新原本的紀錄
def save_high_latency_recovery(connection, high_latency_id, recovery_time, duration_seconds, peak_latency_ms):
    cursor = connection.cursor()

    sql = """
        UPDATE `high_latency_events`
        SET `recovery_time` = %s,
            `duration_seconds` = %s,
            `peak_latency_ms` = %s
        WHERE `id` = %s
    """

    cursor.execute(sql, (recovery_time, duration_seconds, peak_latency_ms, high_latency_id))
    connection.commit()
    cursor.close()


# 查詢高延遲異常事件紀錄
def get_high_latency_events(connection, limit=100):
    cursor = connection.cursor(dictionary = True)

    sql = """
        SELECT * FROM `high_latency_events`
        ORDER BY `id` DESC
        LIMIT %s
    """

    cursor.execute(sql,(limit,))
    result = cursor.fetchall()
    cursor.close()

    return result