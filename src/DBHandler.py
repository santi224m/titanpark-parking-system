import os

import psycopg2
from dotenv import load_dotenv

# Load .env variables
load_dotenv()

class DBHandler:
	def __enter__(self):
		database_url = os.getenv("DATABASE_URL")
		if database_url:
			self.conn = psycopg2.connect(database_url)
		else:
			self.conn = psycopg2.connect(
				dbname='titanpark_parking_system',
				user=os.getenv('DB_USER', 'postgres'),
				password=os.getenv('DB_PASSWORD'),
				host=os.getenv('DB_HOST', 'localhost'),
				port=os.getenv('DB_PORT', '5432'),
			)
		self.curr = self.conn.cursor()
		return self.curr

	def __exit__(self, exc_type, exc_value, exc_tb):
		self.conn.commit()
		self.conn.close()
