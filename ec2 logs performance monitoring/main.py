import subprocess
import time

print("Starting consumer...")
subprocess.Popen(["python", "scripts/consumer.py"])

time.sleep(5)

print("Starting producer...")
subprocess.Popen(["python", "scripts/producer.py"])