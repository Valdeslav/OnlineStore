import psycopg2
import peewee

def con_db():
	con = psycopg2.connect(
		database="store_db",
		user="postgres",
		password="dkflbr",
		host="onlinestore_postgres_1"
		)
	return con

