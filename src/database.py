import os
import psycopg2

# Connects to the local PostgreSQL container mapped to port 5432
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://revolut_user:revolut_password@localhost:5432/transactions_db",
)


def get_connection():
    return psycopg2.connect(DATABASE_URL)


def init_db():
    query = """
    CREATE TABLE IF NOT EXISTS transactions (
        transaction_id VARCHAR(64) PRIMARY KEY,
        user_id VARCHAR(64) NOT NULL,
        amount NUMERIC(12, 2) NOT NULL,
        currency VARCHAR(3) NOT NULL,
        status VARCHAR(20) NOT NULL,
        processed_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
    );
    CREATE INDEX IF NOT EXISTS idx_user_id ON transactions (user_id);
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query)
        conn.commit()