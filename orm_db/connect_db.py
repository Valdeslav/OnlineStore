import peewee

def con_db():
	dbhandle = peewee.PostgresqlDatabase(
		"online_store",
		user="postgres",
		password="dkflbr",
		#host="onlinestore_postgres_1"
		host="localhost"
		)
	return dbhandle
