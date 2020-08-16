import psycopg2
from psycopg2.errors import CheckViolation, ForeignKeyViolation

from connect_db import con_db


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
	return int(saved_cart[0])
	

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
	return saved_item


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
	return cart


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
	cart_items=cur.fetchall()
	return cart_items

