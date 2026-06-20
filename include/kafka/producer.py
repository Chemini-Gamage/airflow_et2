from kafka import KafkaProducer
import pandas as pd
import json
import time

# Load dataset
df = pd.read_csv("data/Ecommerce Order Dataset/train/df_Orders.csv")

# Kafka Producer
producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

for _, row in df.iterrows():
    message = row.to_dict()

    producer.send("ecommerce_orders", value=message)

    print("Sent:", message["order_id"])
    time.sleep(0.1)  # simulate streaming

producer.flush()
producer.close()