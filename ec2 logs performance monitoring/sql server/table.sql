CREATE DATABASE ec2_monitoring;
GO

USE ec2_monitoring;
GO

CREATE TABLE ec2_logs (
    id INT IDENTITY(1,1) PRIMARY KEY,
    timestamp DATETIME,
    instance_id VARCHAR(50),
    region VARCHAR(50),
    service VARCHAR(100),
    log_level VARCHAR(20),
    cpu_usage_percent FLOAT,
    memory_usage_percent FLOAT,
    request_latency_ms FLOAT,
    processing_status VARCHAR(20),
    request_id VARCHAR(100)
);


SELECT COUNT(*) AS total_logs
FROM ec2_logs;
