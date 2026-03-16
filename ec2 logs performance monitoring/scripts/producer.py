import pandas as pd
import json
import time
import os
from kafka import KafkaProducer
from dotenv import load_dotenv

load_dotenv()

KAFKA_SERVER = os.getenv("KAFKA_BOOTSTRAP_SERVERS")
TOPIC = os.getenv("KAFKA_TOPIC")

producer = KafkaProducer(
    bootstrap_servers=KAFKA_SERVER,
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

df = pd.read_csv("data/ec2_logs_processing.csv")

print("Producer started...")

for _, row in df.iterrows():

    message = {
        "timestamp": row["timestamp"],
        "instance_id": row["instance_id"],
        "region": row["region"],
        "service": row["service"],
        "log_level": row["log_level"],
        "cpu_usage_percent": row["cpu_usage_percent"],
        "memory_usage_percent": row["memory_usage_percent"],
        "request_latency_ms": row["request_latency_ms"],
        "processing_status": row["processing_status"],
        "request_id": row["request_id"]
    }

    producer.send(TOPIC, message)

    print("Sent:", message)

    time.sleep(1)

producer.flush()