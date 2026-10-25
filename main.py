from fastapi import FastAPI, Query
from database import get_connection
from ping_collector import get_ping_stats
from ping_collector import get_recent_records
from ping_collector import get_hourly_stats
from database import get_anomaly_events
from database import get_high_latency_events

# cd .\network-latency-monitor
# python -m uvicorn main:app --reload


app = FastAPI()

# 查詢全部歷史紀錄的統計(ping值成功率)
@app.get("/api/ping/stats")
def ping_stats():
    connection = get_connection()

    try:
        stats = get_ping_stats(connection)

        return {
            'total_count': stats['total_count'],
            'success_count': stats['success_count'],
            'failure_count': stats['failure_count'],
            'success_rate': (
                float(stats['success_rate'])
                if stats["success_rate"] is not None
                else None
            ),
            'failure_rate': (
                float(stats['failure_rate'])
                if stats['failure_rate'] is not None
                else None
            )
        }
    finally:
        connection.close()


# 查詢最近 N 筆 Ping 紀錄
@app.get("/api/ping/records")
def ping_records(limit: int = Query(default=10, ge =1, le = 100)):
    connection = get_connection()

    try:
        records = get_recent_records(connection, limit)

        return records

    finally:
        connection.close()


# 回傳最近 N 小時的統計結果
@app.get("/api/ping/stats/hourly")
def hourly_stats(hours: int = Query(default=1, ge=1, le=168)):
    connection = get_connection()

    try:
        stats = get_hourly_stats(connection,hours)

        return stats

    finally:
        connection.close()

# 取得異常紀錄
@app.get("/api/anomalies")
def read_anomalies(limit: int = 100):
    connection = get_connection()

    try:
        anomalies = get_anomaly_events(connection, limit)
        return anomalies
    
    finally:
        connection.close()


# 取得高延遲異常紀錄
@app.get("/api/high-latency")
def read_high_latency_events(limit: int = Query(default=100, ge=1, le=1000)):
    connection = get_connection()

    try:
        high_latency_events = get_high_latency_events(connection, limit)
        return high_latency_events

    finally:
        connection.close()