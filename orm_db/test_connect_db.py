import peewee

def con_db():
	dbhandle = peewee.PostgresqlDatabase(
		"store_db",
		user="postgres",
		password="dkflbr",
		host="onlinestore_postgres_1"
		)
	return dbhandle