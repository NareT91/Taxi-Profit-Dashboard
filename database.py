
import os
import psycopg
from dotenv import load_dotenv

load_dotenv()


def create_database():
    database_url = os.getenv("DATABASE_URL")

    if not database_url:
        raise RuntimeError("DATABASE_URL is missing from .env")

    with psycopg.connect(database_url) as connection:
        with connection.cursor() as cursor:

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id BIGSERIAL PRIMARY KEY,
                    fullname TEXT NOT NULL,
                    email TEXT NOT NULL UNIQUE,
                    password_hash TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS taxi_records (
                    id BIGSERIAL PRIMARY KEY,
                    user_id BIGINT NOT NULL REFERENCES users(id),
                    taxi_name TEXT NOT NULL,
                    month TEXT NOT NULL,
                    income DOUBLE PRECISION NOT NULL,
                    expenses DOUBLE PRECISION NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS taxi_targets (
                    id BIGSERIAL PRIMARY KEY,
                    user_id BIGINT NOT NULL REFERENCES users(id),
                    taxi_name TEXT NOT NULL,
                    month TEXT NOT NULL,
                    target DOUBLE PRECISION NOT NULL,
                    UNIQUE (user_id, taxi_name, month)
                )
            """)

    print("Neon database and tables created successfully!")


if __name__ == "__main__":
    create_database()