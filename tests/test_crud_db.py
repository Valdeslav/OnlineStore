import psycopg2
import pytest

import crud_db.db as db

def test_save_cart():
	cart = db.save_cart()
	value = len(cart) == 2 and'id' in cart.keys() and 'items' in cart.keys() and\
			type(cart['id']) == int and cart['items'] == []
	assert value == True


@pytest.mark.parametrize("inp_item, exp_item",
						[({'product': 'milk', 'quantity': 1, 'cart_id': 20},
						  {'product': 'milk', 'quantity': 1, 'cart_id': 20, 'id': int}),

						 ({'product': 'shoes', 'quantity': 2, 'cart_id': 3},
						  False),

						  ({'product': 'prod', 'quantity': 0, 'cart_id': 20},
						  False),

						 ({'product': 'some product', 'quantity': 100, 'cart_id': 20},
						  {'product': 'some product', 'quantity': 100, 'cart_id': 20, 'id': int})

						])
def test_save_item(inp_item, exp_item):
	item = db.save_item(inp_item)
	if item:
		item['id'] = type(item['id'])
	assert item == exp_item

@pytest.mark.parametrize("inp, outp", [(20, True), (1, False)])
def test_check_cart(inp, outp):
	assert db.check_cart(inp) == outp

@pytest.mark.parametrize("inp, value", 
						[(db.save_item({'product': 'p', 'quantity': 2, 'cart_id': 20})['id'], 1),
						 (1, 0)])
def test_remove_item(inp, value):
	assert db.remove_item(inp) == value


@pytest.mark.parametrize("inp, exp_task", [
						 (17, {'id': 17, 'items': []}),
						 (18, {'id': 18, 'items': 
						 	[{'id': 64, 'product': 'prod1', 'quantity': 3, 'cart_id': 18},
						 	 {'id': 65, 'product': 'prod2', 'quantity': 7, 'cart_id': 18}]})
						 ])
def test_get_cart(inp, exp_task):
	assert db.get_cart(inp) == exp_task