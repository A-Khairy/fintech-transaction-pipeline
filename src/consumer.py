import json
import logging
from kafka import KafkaConsumer
from src.database import get_connection, init_db
from src.models import Transaction

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("TransactionConsumer")


def evaluate_transaction(tx: Transaction) -> str:
    """Business rule: large amounts require manual compliance review."""
    if tx.amount >= 10_000.0:
        return "FLAGGED_REVIEW"
    return "SETTLED"


def save_transaction(tx: Transaction, status: str):
    """Idempotent insert into PostgreSQL using ON CONFLICT."""
    query = """
    INSERT INTO transactions (transaction_id, user_id, amount, currency, status)
    VALUES (%s, %s, %s, %s, %s)
    ON CONFLICT (transaction_id) DO NOTHING;
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                query,
                (
                    tx.transaction_id,
                    tx.user_id,
                    tx.amount,
                    tx.currency.value,
                    status,
                ),
            )
        conn.commit()


def run_consumer():
    init_db()
    consumer = KafkaConsumer(
        "payment_events",
        bootstrap_servers=["localhost:29092"],
        group_id="ledger-group",
        auto_offset_reset="earliest",
        enable_auto_commit=True,
        api_version=(2, 8, 1),
        value_deserializer=lambda m: json.loads(m.decode("utf-8")),
    )
    logger.info("Transaction Consumer connected and listening on localhost:29092...")

    for message in consumer:
        raw_data = message.value
        try:
            tx = Transaction(**raw_data)
            status = evaluate_transaction(tx)
            save_transaction(tx, status)
            logger.info(f"Processed {tx.transaction_id} -> {status}")
        except Exception as e:
            logger.error(f"Failed processing message: {raw_data} | Error: {e}")


if __name__ == "__main__":
    run_consumer()