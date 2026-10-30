
CREATE TABLE IF NOT EXISTS ping_records (
    id INT NOT NULL AUTO_INCREMENT,
    timestamp DATETIME NOT NULL,
    latency_ms FLOAT DEFAULT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS anomaly_events (
    id INT NOT NULL AUTO_INCREMENT,
    start_time DATETIME NOT NULL,
    recovery_time DATETIME DEFAULT NULL,
    duration_seconds FLOAT DEFAULT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS high_latency_events (
    id INT NOT NULL AUTO_INCREMENT,
    start_time DATETIME NOT NULL,
    recovery_time DATETIME DEFAULT NULL,
    duration_seconds FLOAT DEFAULT NULL,
    peak_latency_ms INT NOT NULL,
    threshold_ms INT NOT NULL,
    PRIMARY KEY (id)
);
