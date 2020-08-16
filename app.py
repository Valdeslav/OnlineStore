from flask import Flask, jsonify, abort, make_response, request

import db
app = Flask(__name__)

@app.errorhandler(404)
def not_found(error):
	return make_response(jsonify({'error': 'Cart not found'}))


@app.errorhandler(400)
def bad_request(error):
	return make_response(jsonify({'error': 'product is null or quantity <= 0'}))


@app.route('/online-store/api/carts/<int:cart_id>', methods=['GET'])
def get_cart(cart_id):
	if db.check_cart(cart_id):
		cart = db.get_cart(cart_id)
		cart_items = []
		for item in cart:
			cart_item = {}
			cart_item['id'] = item[0]
			cart_item['product'] = item[1]
			cart_item['quantity'] = item[2]
			cart_item['cart_id'] = item[3]
			cart_items.append(cart_item)
		return jsonify({'id': cart_id,
						'items': cart_items})
	else:
		abort(404)


@app.route('/online-store/api/carts', methods=['POST'])
def create_cart():
	cart_id = db.save_cart()
	return jsonify({'id': cart_id, 'items': []}), 201


@app.route('/online-store/api/carts/<int:cart_id>/items', methods=['POST'])
def add_item(cart_id):
	if not db.check_cart(cart_id):
		abort(404)
	if not request.json or not 'product' in request.json or\
	   not 'quantity' in request.json or request.json['product'] == "":
		abort(400)
	item = {
		'product': request.json['product'],
		'quantity': request.json['quantity'],
		'cart_id': cart_id
	}
	saved_item = db.save_item(item)
	if not saved_item :
		abort(400)
	item_dict = {}
	item_dict['id'] = saved_item[0]
	item_dict['product'] = saved_item[1]
	item_dict['quantity'] = saved_item[2]
	item_dict['cart_id'] = saved_item[3]
	return jsonify(item_dict), 201


@app.route('/online-store/api/carts/<int:cart_id>/items/<int:item_id>', methods=['DELETE'])
def delete_cart_item(cart_id, item_id):
	if not db.check_cart(cart_id):
		abort(404)
	deleted = db.remove_item(item_id)
	if deleted:
		return jsonify({'result': True})
	return jsonify({'error': 'Cart_item not found'})

if __name__ == '__main__':
	app.run(debug=True)

