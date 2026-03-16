import json
import os
import pyodbc
from kafka import KafkaConsumer
from dotenv import load_dotenv

# load env
load_dotenv()

KAFKA_SERVER = os.getenv("KAFKA_BOOTSTRAP_SERVERS")
TOPIC = os.getenv("KAFKA_TOPIC")

SQL_SERVER = os.getenv("SQL_SERVER")
SQL_DATABASE = os.getenv("SQL_DATABASE")

# Connect to SQL Server using Windows Authentication
conn = pyodbc.connect(
    f"DRIVER={{ODBC Driver 17 for SQL Server}};"
    f"SERVER={SQL_SERVER};"
    f"DATABASE={SQL_DATABASE};"
    f"Trusted_Connection=yes;"
)

cursor = conn.cursor()

print("Connected to SQL Server")

# Kafka consumer
consumer = KafkaConsumer(
    TOPIC,
    bootstrap_servers=KAFKA_SERVER,
    value_deserializer=lambda x: json.loads(x.decode("utf-8"))
)

print("Listening to Kafka topic...")

for message in consumer:

    data = message.value

    print("Received:", data)

    cursor.execute(
        """
        INSERT INTO ec2_logs (
            timestamp,
            instance_id,
            region,
            service,
            log_level,
            cpu_usage_percent,
            memory_usage_percent,
            request_latency_ms,
            processing_status,
            request_id
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        data["timestamp"],
        data["instance_id"],
        data["region"],
        data["service"],
        data["log_level"],
        data["cpu_usage_percent"],
        data["memory_usage_percent"],
        data["request_latency_ms"],
        data["processing_status"],
        data["request_id"]
    )

    conn.commit()

    print("Inserted into SQL Server")