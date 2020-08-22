from flask import Flask, jsonify, abort, make_response, request

import orm_db.db as db

def make_api(app):
	@app.errorhandler(404)
	def not_found(error):
		return make_response(jsonify({'error': 'Cart not found'}), 404)


	@app.errorhandler(400)
	def bad_request(error):
		return make_response(jsonify({'error': 'product is null or quantity <= 0'}), 400)


	@app.route('/online-store/api/carts/<int:cart_id>', methods=['GET'])
	def get_cart(cart_id):
		if db.check_cart(cart_id):
			cart = db.get_cart(cart_id)
			return jsonify(cart)
		else:
			abort(404)


	@app.route('/online-store/api/carts', methods=['POST'])
	def create_cart():
		cart = db.save_cart()
		return jsonify(cart), 201


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
		return saved_item, 201


	@app.route('/online-store/api/carts/<int:cart_id>/items/<int:item_id>', methods=['DELETE'])
	def delete_item(cart_id, item_id):
		if not db.check_cart(cart_id):
			abort(404)
		deleted = db.remove_item(item_id)
		if deleted:
			return jsonify({'result': True})
		return jsonify({'error': 'Cart_item not found'}), 404

if __name__ == '__main__':
	app = Flask(__name__)
	make_api(app)
	app.run(debug=True, host='0.0.0.0', port=5000)

