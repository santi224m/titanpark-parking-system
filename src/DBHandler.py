import os

import psycopg2
from dotenv import load_dotenv

# Load .env variables
load_dotenv()

class DBHandler:
	def __enter__(self):
		self.conn = psycopg2.connect(
			database='titanpark_parking_system',
			user='postgres',
			password=os.getenv('DB_PASSWORD')
		)
		self.curr = self.conn.cursor()
		return self.curr

	def __exit__(self, exc_type, exc_value, exc_tb):
		self.conn.commit()
		self.conn.close()