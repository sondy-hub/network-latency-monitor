# Network Latency Monitor

A Python-based backend application for monitoring network latency, storing Ping records in MySQL, and detecting network anomalies.

The project uses FastAPI to provide REST APIs, Docker Compose to manage services, and GitHub Actions for automated testing.

## Features

- Periodically measure network latency using Ping
- Store monitoring records in MySQL
- Detect consecutive Ping failures
- Detect high-latency events
- Track anomaly start and recovery times
- Provide monitoring data through REST APIs
- Run automated unit and integration tests with Pytest
- Deploy services using Docker Compose
- Preserve MySQL data using Docker volumes
- Automatically execute tests with GitHub Actions

## Tech Stack

| Category | Technology |
|---|---|
| Language | Python |
| Backend Framework | FastAPI |
| Database | MySQL 8 |
| Containerization | Docker, Docker Compose |
| Testing | Pytest |
| CI | GitHub Actions |
| Version Control | Git, GitHub |

## System Architecture

```text
             Network Target
                   |
                   | Ping
                   v
             Ping Collector
                   |
                   | Store records and events
                   v
                 MySQL
                   ^
                   | Query records
                   |
               FastAPI
                   |
                   | REST API
                   v
              API Clients
```

Docker Compose manages three services:

- `db`: MySQL database
- `api`: FastAPI application
- `collector`: Network latency monitoring process

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/sondy-hub/network-latency-monitor.git
cd network-latency-monitor
```

### 2. Configure Environment Variables

Create a `.env` file based on `.env.example`.

Configure the database credentials, Ping target, and high-latency threshold.

Do not commit `.env` to Git.

### 3. Start the Application

Make sure Docker Desktop or Docker Engine with Docker Compose is available.

```bash
docker compose up -d --build
```

### 4. Access the API Documentation

Open:

http://localhost:8000/docs

FastAPI provides interactive API documentation through Swagger UI.

### 5. Stop the Application

```bash
docker compose down
```

The MySQL named volume preserves database data when the containers are stopped and removed normally.

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/ping/records` | Retrieve recent Ping records |
| GET | `/api/ping/stats` | Retrieve overall Ping statistics |
| GET | `/api/ping/stats/hourly` | Retrieve statistics for recent hours |
| GET | `/api/anomalies` | Retrieve connection failure events |
| GET | `/api/high-latency` | Retrieve high-latency events |

## Testing

The project uses Pytest for automated unit and integration testing.

### Run Unit Tests

```bash
python -m pytest -m "not integration" -v
```

### Run Database Integration Tests

Integration tests use a dedicated MySQL test database named `network_monitor_test`.

They require the `RUN_DB_INTEGRATION_TESTS=1` flag and appropriate `TEST_DB_*` environment variables.

### Continuous Integration

GitHub Actions automatically runs tests when code is pushed or a pull request is created.

The CI workflow starts a temporary MySQL service, initializes the test database, and runs the test suite.

Latest verified result: **13 tests passed**.

## Project Status

**Status: V2 Completed**

### Completed

- Network latency collection
- MySQL data storage
- FastAPI REST APIs
- Network failure detection
- High-latency event detection
- Docker containerization
- Docker Compose orchestration
- MySQL data persistence
- Pytest unit testing
- MySQL integration testing
- GitHub Actions CI
