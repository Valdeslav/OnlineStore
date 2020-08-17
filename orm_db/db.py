from peewee import *


dbhandle = PostgresqlDatabase(
		"store_db",
		user="postgres",
		password="dkflbr",
		host="onlinestore_postgres_1"
		)