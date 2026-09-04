import json
import random
import time
import uuid
from datetime import datetime, timezone
from kafka import KafkaProducer


def run_producer():
    producer = KafkaProducer(
        bootstrap_servers=["localhost:29092"],
        api_version=(2, 8, 1),
        value_serializer=lambda v: json.dumps(v).encode("utf-8"),
    )
    currencies = ["EUR", "USD", "GBP"]
    print("Producer initialized. Streaming transactions to Kafka...")

    while True:
        payload = {
            "transaction_id": str(uuid.uuid4()),
            "user_id": f"usr-{random.randint(100, 999)}",
            # Generate amounts; occasionally trigger the >10,000 FLAGGED_REVIEW rule
            "amount": round(random.uniform(10.0, 15000.0), 2),
            "currency": random.choice(currencies),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
        producer.send("payment_events", value=payload)
        print(
            f"[PRODUCED] ID: {payload['transaction_id'][:8]}... | "
            f"{payload['amount']:>8.2f} {payload['currency']} | User: {payload['user_id']}"
        )
        time.sleep(1.5)


if __name__ == "__main__":
    run_producer()