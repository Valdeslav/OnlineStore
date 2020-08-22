from peewee import *

from orm_db.test_connect_db import con_db

dbhandle = con_db()

class BaseModel(Model):
	class Meta:
		database = dbhandle


class Cart(BaseModel):
	id = PrimaryKeyField(null=False)

	class Meta:
		db_table = "cart"
		order_by = ('id',)

class Cart_item(BaseModel):
	id = PrimaryKeyField(null=False)
	product = CharField(max_length=100)
	quantity = IntegerField(null=False, constraints=[Check('quantity > 0')])
	cart = ForeignKeyField(Cart, related_name='fk_cart_item',
						   to_field='id', on_delete='restrict', on_update='cascade')
	class Meta:
		db_table="cart_item"
		order_by=('id',)