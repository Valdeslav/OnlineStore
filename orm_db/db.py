import peewee
from orm_db.models import *
from psycopg2.errors import CheckViolation

def init_db():
	try:
		dbhandle.connect()
		Cart.create_table()
		Cart_item.create_table()
	except peewee.InternalError as px:
		print(str(px))

def save_cart():
	row = Cart()
	row.save()
	return {'id': row.id, 'items': []}

def save_item(item):
	try:
		cart = Cart.select().where(Cart.id == item['cart_id']).get()
	except DoesNotExist as de:
		return False
	if item['quantity'] <= 0:
		return False
	row = Cart_item(
					product=item['product'],
					quantity=item['quantity'],
					cart=cart)
	row.save()
	item_dict = {}
	item_dict['id'] = row.id
	item_dict['product'] = row.product
	item_dict['quantity'] = row.quantity
	item_dict['cart_id'] = row.cart.id
	return item_dict

def check_cart(cart_id):
	try:
		cart = Cart.get(Cart.id == cart_id)
	except DoesNotExist as de:
		return False
	return True

def remove_item(item_id):
	try:
		cart_item = Cart_item.get(Cart_item.id == item_id)
	except DoesNotExist as de:
		return False
	cart_item.delete_instance()
	return True

def get_cart(cart_id):
	cart = Cart_item.select().where(Cart_item.cart == cart_id)
	cart_items = []
	for item in cart:
		cart_item = {}
		cart_item['id'] = item.id
		cart_item['product'] = item.product
		cart_item['quantity'] = item.quantity
		cart_item['cart_id'] = item.cart.id
		cart_items.append(cart_item)
	return {'id': cart_id,
		   'items': cart_items}
