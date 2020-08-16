import psycopg2

def con_db():
	con = psycopg2.connect(
		database="online_store",
		user="postgres",
		password="dkflbr",
		host="localhost"
		)
	return con;