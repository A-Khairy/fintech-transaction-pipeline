# Real-Time Financial Transaction Pipeline

[![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python)](https://www.python.org/)
[![Kafka](https://img.shields.io/badge/Apache_Kafka-7.5.0-black?logo=apachekafka)](https://kafka.apache.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-336791?logo=postgresql)](https://www.postgresql.org/)
[![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?logo=docker)](https://www.docker.com/)
[![Testing](https://img.shields.io/badge/Tests-Pytest-yellow?logo=pytest)](https://docs.pytest.org/)

An event-driven transaction ingestion microservice simulating real-time payment processing. Built with Python 3, Apache Kafka, and PostgreSQL, following Test-Driven Development (TDD) best practices.

---

## Architecture Overview
[ Mock Payment Producer ]
│
│ (JSON Streams)
▼
[ Apache Kafka Topic: payment_events ]
│
▼
[ Transaction Consumer Worker ]
├── 1. Schema Validation (Pydantic)
├── 2. Compliance Evaluation Rules
│        ├── Amount >= 10k ──► FLAGGED_REVIEW
│        └── Amount < 10k  ──► SETTLED
└── 3. Idempotent Storage (PostgreSQL)
--------------------

## Features

- **Event-Driven Processing:** Decoupled producer-consumer architecture using Apache Kafka and consumer groups.
- **Strict Schema Enforcement:** Transaction payloads validated via Pydantic (`amount > 0`, ISO timestamps, regulatory caps).
- **Idempotent Ingestion:** Safe writes into PostgreSQL utilizing `ON CONFLICT (transaction_id) DO NOTHING` to prevent duplicate ledger records.
- **Test-Driven Development:** Complete test coverage on compliance rules and edge cases via Pytest.
- **Containerized Infrastructure:** One-command setup for Zookeeper, Kafka, and PostgreSQL using Docker Compose.

--------------

## Tech Stack

- **Language:** Python 3.12
- **Message Broker:** Apache Kafka (Confluent Platform 7.5.0) & Zookeeper
- **Database:** PostgreSQL 15
- **Data Validation:** Pydantic v2
- **Testing:** Pytest
- **Infrastructure:** Docker & Docker Compose

-----------

## Getting Started

### Prerequisites

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) (running)
- Python 3.10+
- Git

### 1. Clone & Set Up Virtual Environment

```bash
git clone [https://github.com/A-Khairy/fintech-transaction-pipeline.git](https://github.com/A-Khairy/fintech-transaction-pipeline.git)
cd fintech-transaction-pipeline

python -m venv venv
# On Windows:
.\venv\Scripts\Activate.ps1
# On Linux/macOS:
# source venv/bin/activate

pip install -r requirements.txt
--------------------
2. Launch Infrastructure
Spin up Kafka, Zookeeper, and PostgreSQL in detached mode:
docker compose up -d
--------------------------
Verify all three containers are active:
docker compose ps
--------------------------
3. Run the Test Suite (TDD)
Execute the unit tests validating validation logic and risk thresholds:
pytest tests/ -v
--------------------------
4. Run the Pipeline
Open two terminal windows (with venv activated in both):

Terminal 1 (Consumer Worker):
python -m src.consumer
---------------------------
Terminal 2 (Mock Payment Producer):
python -m src.producer
------------------------------
Verifying PostgreSQL Data
Inspect ingested transactions directly from the database container:
docker compose exec postgres psql -U revolut_user -d transactions_db -c "SELECT transaction_id, user_id, amount, currency, status, processed_at FROM transactions ORDER BY processed_at DESC LIMIT 
10;"
----------------------
Teardown
To shut down containers and networks without losing database data:
docker compose down
------------------