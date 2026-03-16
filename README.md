# EC2 Logs Performance Monitoring Pipeline

## Project Overview

This project simulates a **real-time EC2 log monitoring pipeline** using **Kafka, Python, SQL Server, and Power BI**.

The system streams log data from a CSV dataset through **Apache Kafka**, processes it with a **Python consumer**, stores it in **Microsoft SQL Server**, and visualizes the metrics in a **Power BI dashboard**.

### Data Pipeline Architecture

```text
CSV Dataset
     │
     ▼
Kafka Producer (Python)
     │
     ▼
Kafka Topic
     │
     ▼
Kafka Consumer (Python)
     │
     ▼
SQL Server Database
     │
     ▼
Power BI Dashboard
```

---

# Repository

GitHub Repository:

https://github.com/ozandx/ec2-logs-performance-monitoring

---

# Project Structure

```
ec2-logs-performance-monitoring
│
├── data
│   └── ec2_logs_processing.csv
│
├── scripts
│   ├── producer.py
│   └── consumer.py
│
├── sql server
│   └── table.sql
│
├── .env
├── docker-compose.yml
├── main.py
├── requirements.txt
└── README.md
```

---

# Technologies Used

* Python
* Apache Kafka
* Docker
* Microsoft SQL Server
* Power BI
* Pandas
* PyODBC

---

# Prerequisites

Before running the project, install the following:

* Python 3.9+
* Docker & Docker Compose
* Microsoft SQL Server
* Power BI Desktop
* ODBC Driver 17 for SQL Server
* Git

---

# Step 1 — Clone the Repository

Clone the project from GitHub:

```bash
git clone https://github.com/ozandx/ec2-logs-performance-monitoring.git
```

Navigate to the project folder:

```bash
cd ec2-logs-performance-monitoring
```

---

# Step 2 — Install Python Dependencies

Install required packages:

```bash
pip install -r requirements.txt
```

Dependencies:

```
kafka-python
pandas
python-dotenv
pyodbc
```

---

# Step 3 — Configure Environment Variables

Create a `.env` file in the root directory.

Example configuration:

```
KAFKA_BOOTSTRAP_SERVERS=localhost:9092
KAFKA_TOPIC=ec2_logs

SQL_SERVER=DESKTOP-APH7COF\SQLEXPRESS
SQL_DATABASE=ec2_monitoring
```

Update the **SQL Server name** according to your machine.

---

# Step 4 — Start Kafka with Docker

Run:

```bash
docker-compose up -d
```

This starts:

* Zookeeper
* Kafka Broker

Verify containers:

```bash
docker ps
```

---

# Step 5 — Create SQL Server Database

Open **SQL Server Management Studio (SSMS)** and run:

```sql
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
```

Verify table creation:

```sql
SELECT COUNT(*) AS total_logs
FROM ec2_logs;
```

---

# Step 6 — Run the Data Pipeline

Run the main script:

```bash
python main.py
```

This script automatically:

1. Starts the **Kafka Consumer**
2. Waits **5 seconds**
3. Starts the **Kafka Producer**

---

# Step 7 — Data Streaming (Producer)

`producer.py` reads the dataset:

```
data/ec2_logs_processing.csv
```

Each row is converted to JSON and sent to the Kafka topic.

Example message:

```json
{
  "timestamp": "2024-01-01 10:00:00",
  "instance_id": "i-2345abc",
  "region": "us-east-1",
  "service": "auth-service",
  "log_level": "INFO",
  "cpu_usage_percent": 45.3,
  "memory_usage_percent": 60.2,
  "request_latency_ms": 210,
  "processing_status": "SUCCESS",
  "request_id": "req-123"
}
```

---

# Step 8 — Kafka Consumer → SQL Server

`consumer.py` listens to the Kafka topic and inserts messages into SQL Server.

Pipeline:

```
Kafka → Python Consumer → SQL Server Table (ec2_logs)
```

Console output example:

```
Connected to SQL Server
Listening to Kafka topic...
Received: {...}
Inserted into SQL Server
```

---

# Step 9 — Verify Data in SQL Server

Run:

```sql
SELECT * FROM ec2_logs;
```

or

```sql
SELECT COUNT(*) FROM ec2_logs;
```

---

# Step 10 — Connect Power BI Dashboard

Open **Power BI Desktop**.

Steps:

1. Click **Get Data**
2. Select **SQL Server**
3. Enter:

```
Server: DESKTOP-APH7COF\SQLEXPRESS
Database: ec2_monitoring
```

4. Select table:

```
ec2_logs
```

Load the data and create visualizations.

---

# Dashboard Metrics

The Power BI dashboard visualizes:

### System Performance

* CPU usage trend
* Memory usage trend
* Request latency

### Log Level Distribution

* INFO
* DEBUG
* WARN
* ERROR

### Requests by Service and Region

Services:

* api-gateway
* auth-service
* payment-service
* data-processor
* user-service

Regions:

* ap-southeast-1
* eu-west-1
* us-east-1
* us-west-2

### Processing Status

* SUCCESS
* FAILED
* RETRY

---

# Stop the Services

Stop Kafka containers:

```bash
docker-compose down
```

---

# Author

Ozan D

GitHub: https://github.com/ozandx
