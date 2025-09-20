import psycopg2

class DBHandler:
	def __enter__(self):
		self.conn = psycopg2.connect(database='titanpark_parking_system', user='postgres')
		self.curr = self.conn.cursor()
		return self.curr

	def __exit__(self, exc_type, exc_value, exc_tb):
		self.conn.commit()
		self.conn.close()