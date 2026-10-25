# python -m pytest -v

from datetime import datetime
from datetime import timedelta
from anomaly_detector import HighLatencyTracker


def test_normal_ping():
    tracker = HighLatencyTracker(threshold=70)

    timestamp = datetime(2026, 10, 19, 12, 0, 0)

    event = tracker.process_ping(25, timestamp)

    assert event is None
    assert tracker.is_anomaly is False



def test_high_latency_started():
    tracker = HighLatencyTracker(threshold=70)

    timestamp = datetime(2026, 10, 19, 12, 0, 0)
    event = tracker.process_ping(70, timestamp)

    assert event["type"] == "high_latency_started"
    assert event["start_time"] == timestamp
    assert event["peak_latency_ms"] == 70
    assert tracker.is_anomaly


ping_results = [120, 250, 180, 350]

def test_high_latency_continues():
    tracker = HighLatencyTracker(threshold = 70)

    t0 = datetime(2026, 10, 19, 12, 0, 0)

    event1 = tracker.process_ping(120, t0)

    event2 = tracker.process_ping(250, t0 + timedelta(seconds=2))

    event3 = tracker.process_ping(180, t0 + timedelta(seconds=4))

    event4 = tracker.process_ping(350, t0 + timedelta(seconds=6))

    assert event2 is None
    assert event3 is None
    assert event4 is None

    assert tracker.is_anomaly is True
    assert tracker.peak_latency_ms == 350



def test_high_latency_recovered():
    tracker = HighLatencyTracker(threshold=70)

    t0 = datetime(2026, 10, 19, 12, 0, 0)

    tracker.process_ping(120, t0)
    tracker.process_ping(250, t0 + timedelta(seconds=2))
    tracker.process_ping(180, t0 + timedelta(seconds=4))

    event = tracker.process_ping(35, t0 + timedelta(seconds=6))

    assert event["type"] == "high_latency_recovered"
    assert event["start_time"] == t0
    assert event["recovery_time"] == t0 + timedelta(seconds=6)
    assert event["duration_seconds"] == 6.0
    assert event["peak_latency_ms"] == 250
    assert not tracker.is_anomaly


def test_high_latency_with_none():
    tracker = HighLatencyTracker(threshold=70)

    t0 = datetime(2026, 10, 19, 12, 0, 0)

    tracker.process_ping(120, t0)
    tracker.process_ping(250, t0 + timedelta(seconds=2))

    event = tracker.process_ping(None, t0 + timedelta(seconds=4))

    assert event is None
    assert tracker.is_anomaly
    assert tracker.peak_latency_ms == 250


    tracker.process_ping(180, t0 + timedelta(seconds=6))
    recovery = tracker.process_ping(35, t0 + timedelta(seconds=8))

    assert recovery["type"] == "high_latency_recovered"
    assert recovery["duration_seconds"] == 8.0
    assert recovery["peak_latency_ms"] == 250

    again = tracker.process_ping(80, t0 + timedelta(seconds=8))

    assert again["type"] == "high_latency_started"
