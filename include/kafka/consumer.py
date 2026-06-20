from kafka import KafkaConsumer
import json


def consume_orders(limit=100, bootstrap_servers="kafka:9092", timeout_ms=5000):
    consumer = KafkaConsumer(
        "ecommerce_orders",
        bootstrap_servers=bootstrap_servers,
        value_deserializer=lambda v: json.loads(v.decode("utf-8")),
        auto_offset_reset="earliest",
        enable_auto_commit=True,
        group_id="airflow-group",
        consumer_timeout_ms=timeout_ms,
    )

    messages = []

    for i, msg in enumerate(consumer):
        messages.append(msg.value)
        if i + 1 >= limit:
            break

    consumer.close()
    return messages
