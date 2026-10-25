
# Network Latency Monitor

A Python-based network latency monitoring system with FastAPI, MySQL, anomaly detection, and automated testing.

## Features

- Periodically measure network latency using Ping
- Store monitoring records in MySQL
- Detect consecutive Ping failures
- Detect high-latency events
- Track anomaly start and recovery times
- Provide monitoring data through REST APIs
- Run automated tests with Pytest

## Tech Stack

- Python
- FastAPI
- MySQL
- Pytest
- Git & GitHub

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/ping/records` | Retrieve recent Ping records |
| GET | `/api/ping/stats` | Retrieve overall Ping statistics |
| GET | `/api/ping/stats/hourly` | Retrieve statistics for recent hours |
| GET | `/api/anomalies` | Retrieve connection failure events |
| GET | `/api/high-latency` | Retrieve high-latency events |

## Running Tests

```bash
python -m pytest -v
```

## Project Status

This project is under active development.

Planned improvements:
- Docker containerization
- Linux compatibility
- GitHub Actions CI
- Monitoring dashboard
