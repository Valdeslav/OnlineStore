from datetime import datetime
from peewee import *
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from orm_db.connect_db import con_db


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
		db_table = "cart_item"
		order_by = ('id',)


class User(BaseModel, UserMixin):
	id = PrimaryKeyField(null=False)
	username = CharField(max_length=100, null=False, unique=True)
	email = CharField(max_length=100, null=False, unique=True)
	password_hash = CharField(max_length=100, null=False)
	created_on = DateTimeField(default=datetime.utcnow())
	updated_on = DateTimeField(default=datetime.utcnow())

	def set_password(self, password):
		self.password_hash = generate_password_hash(password)

	def check_password(self, password):
		return check_password_hash(self.password_hash, password)

