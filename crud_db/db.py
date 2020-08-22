import psycopg2
from psycopg2.errors import CheckViolation, ForeignKeyViolation

from crud_db.test_connect_db import con_db


def save_cart():
	con = con_db()
	cur = con.cursor()
	cur.execute(
		"INSERT INTO cart DEFAULT VALUES RETURNING id;"
		)
	saved_cart = cur.fetchone()
	con.commit()
	cur.close()
	con.close()
	cart_id = int(saved_cart[0])
	return {'id': cart_id, 'items': []}
	

def save_item(item):
	con = con_db()
	cur = con.cursor()
	try:
		cur.execute(
			"INSERT INTO cart_item (id, product, quantity, cart_id) VALUES\
			(DEFAULT, %(product)s, %(quantity)s, %(cart_id)s) RETURNING *",
			item
			)
		saved_item = cur.fetchone()
		con.commit()
	except CheckViolation:
		cur.close()
		con.close()
		return False
	except ForeignKeyViolation:
		cur.close()
		con.close()
		return False
	cur.close()
	con.close()
	item_dict = {}
	item_dict['id'] = saved_item[0]
	item_dict['product'] = saved_item[1]
	item_dict['quantity'] = saved_item[2]
	item_dict['cart_id'] = saved_item[3]
	return item_dict


def check_cart(cart_id):
	con = con_db()
	cur = con.cursor()
	cur.execute(
		"SELECT id FROM cart where id=%(cart_id)s", {'cart_id': cart_id}
		)
	cart = cur.fetchone()
	con.commit()
	cur.close()
	con.close()
	if cart:
		return True
	return False


def remove_item(item_id):
	con = con_db()
	cur = con.cursor()
	cur.execute(
		"DELETE FROM cart_item where id=%(item_id)s", {'item_id': item_id}
		)
	count = cur.rowcount
	con.commit()
	cur.close()
	con.close()
	return count


def get_cart(cart_id):
	con = con_db()
	cur = con.cursor()
	cur.execute(
		"SELECT * FROM cart_item where cart_id=%(cart_id)s", {'cart_id': cart_id}
		)
	cart=cur.fetchall()
	cart_items = []
	for item in cart:
		cart_item = {}
		cart_item['id'] = item[0]
		cart_item['product'] = item[1]
		cart_item['quantity'] = item[2]
		cart_item['cart_id'] = item[3]
		cart_items.append(cart_item)
	return {'id': cart_id,
			'items': cart_items}
	return cart_items
	