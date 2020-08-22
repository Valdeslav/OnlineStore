import pytest
from flask import Flask
import json

import orm_db.db as db

@pytest.mark.parametrize("url, exp_task, code", 
						 [('/online-store/api/carts/18',
						 	{
							  "id":18,
							  "items":[
							    {
							      "cart_id": 18, 
							      "id": 64, 
							      "product": "prod1", 
							      "quantity": 3
							    }, 
							    {
							      "cart_id": 18, 
							      "id": 65, 
							      "product": "prod2", 
							      "quantity": 7
							    }
							  ]
							},
							200
							),
						  

						  ('/online-store/api/carts/2',
						  	{
							  "error": "Cart not found"
							},
							404),
						  ])
def test_get_cart(url, exp_task, code, init_test_client):
	client = init_test_client
	response = client.get(url)
	assert response.get_json() == exp_task
	assert response.status_code == code


def test_create_cart(init_test_client):
	client = init_test_client
	response = client.post('/online-store/api/carts')
	cart = response.get_json()
	value = len(cart) == 2 and'id' in cart.keys() and 'items' in cart.keys() and\
			type(cart['id']) == int and cart['items'] == []
	assert value == True
	assert response.status_code == 201

@pytest.mark.parametrize("url, req_json, exp_item, code",
						[('/online-store/api/carts/20/items',
						  {'product': 'milk', 'quantity': 1},
						  {'product': 'milk', 'quantity': 1, 'cart_id': 20, 'id': int},
						  201),
						  
						 ('/online-store/api/carts/3/items',
						  {'product': 'shoes', 'quantity': 2},
						  {'error': 'Cart not found'},
						  404),

						 ('/online-store/api/carts/20/items',
						  {'product': 'prod', 'quantity': 0},
						  {'error': 'product is null or quantity <= 0'},
						  400),
						  
						 ('/online-store/api/carts/20/items',
						  {'product': 'some product', 'quantity': 100},
						  {'product': 'some product', 'quantity': 100, 'cart_id': 20, 'id': int},
						  201)
						])
def test_add_item(url, req_json, exp_item, code, init_test_client):
	client = init_test_client
	req_headers = {
		'Content-Type': 'application/json'
	}
	response = client.post(url, data=json.dumps(req_json), headers=req_headers)
	item = response.get_json()
	if item and 'id' in item.keys():
		item['id'] = type(item['id'])
	assert item == exp_item
	assert response.status_code == code


@pytest.mark.parametrize("inp, exp, code",
						 [
						 	(db.save_item({'product': 'p', 'quantity': 2, 'cart_id': 20})['id'], 
							{'result': True},
						 	200),

						 	(1, 
						 	{'error': 'Cart_item not found'},
						 	404)
						 	])
def test_delete_item(inp, exp, code, init_test_client):
	url = '/online-store/api/carts/20/items/'+str(inp)
	client = init_test_client
	response = client.delete(url)
	assert response.get_json() == exp
	assert response.status_code == code