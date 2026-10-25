# 自動化測試
# python -m pytest -v

from datetime import datetime
from anomaly_detector import AnomalyTracker

def test_normal_ping():
    tracker = AnomalyTracker()

    timestamp = datetime(2026, 10, 14, 21, 0, 0)

    result = tracker.process_ping(25, timestamp)

    # assert，檢查 result 是否為 None

    assert result is None






from datetime import datetime, timedelta

def test_anomaly_started():
    tracker = AnomalyTracker()

    base_time = datetime(2026, 10, 14, 21, 0, 0)

    results = []

    for i in range(4):
        timestamp = base_time + timedelta(seconds=2 * i)
        event = tracker.process_ping(None, timestamp)
        results.append(event)

    # 請在這裡寫 assert
    assert results[0] is None
    assert results[1] is None
    assert results[2]["type"] == "anomaly_started"
    assert results[2]["start_time"] == base_time
    assert results[3] is None



def test_anomaly_recovered():
    tracker = AnomalyTracker()

    base_time = datetime(2026, 10, 14, 21, 0, 0)

    ping_results = [None, None, None, None, 25]

    results = []

    for i, ping in enumerate(ping_results):
        timestamp = base_time + timedelta(seconds =2 * i)
        event = tracker.process_ping(ping, timestamp)
        results.append(event)


    assert results[4]["type"] == "anomaly_recovered"
    assert results[4]["start_time"] == base_time
    assert results[4]["recovery_time"] == base_time + timedelta(seconds=8)
    assert results[4]["duration_seconds"] == (timestamp-base_time).total_seconds()


def test_failure_count_reset():
    tracker = AnomalyTracker()
    base_time = datetime(2026, 10, 14, 21, 0, 0)

    ping_results = [None, None, 25, None, None, None]

    results = []

    for i, ping in enumerate(ping_results):
        timestamp = base_time + timedelta(seconds =2 * i)
        event = tracker.process_ping(ping, timestamp)
        results.append(event)

    assert results[2] is None
    assert results[4] is None
    assert results[5]["type"] == "anomaly_started"
    assert results[5]["start_time"] == base_time + timedelta(seconds =6)
