import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

class DBHandler:
    def __enter__(self):
        url = (os.getenv("DATABASE_URL") or "").strip()
        if url.startswith("postgresql+psycopg2://"):
            url = url.replace("postgresql+psycopg2://", "postgresql://", 1)

        if url:
            self.conn = psycopg2.connect(url)
        else:
            self.conn = psycopg2.connect(
                dbname=os.getenv("DB_NAME", "titanpark_parking_system"),
                user=os.getenv("DB_USER", os.getenv("USER", "postgres")),
                password=os.getenv("DB_PASSWORD"),
                host=os.getenv("DB_HOST", "localhost"),
                port=os.getenv("DB_PORT", "5432"),
            )
        self.conn.autocommit = False
        self.curr = self.conn.cursor()
        return self.curr

    def __exit__(self, exc_type, exc_value, exc_tb):
        try:
            if exc_type:
                self.conn.rollback()
            else:
                self.conn.commit()
        finally:
            self.curr.close()
            self.conn.close()