from flask import Flask, jsonify, abort, make_response, request
from flask_login import (LoginManager, current_user, login_user, logout_user,
                         login_required)

import orm_db.db as db


def make_api(app):
    @app.errorhandler(404)
    def not_found(error):
        return make_response(jsonify({'error': 'Cart not found'}), 404)

    @app.errorhandler(400)
    def bad_request(error):
        return make_response(
            jsonify({'error': 'product is null or quantity <= 0'}), 400)

    @app.route('/online-store/api/carts/<int:cart_id>', methods=['GET'])
    @login_required
    def get_cart(cart_id):
        if db.check_cart(cart_id):
            cart = db.get_cart(cart_id)
            return jsonify(cart)
        else:
            abort(404)

    @app.route('/online-store/api/carts', methods=['POST'])
    @login_required
    def create_cart():
        cart = db.save_cart()
        return jsonify(cart), 201

    @app.route('/online-store/api/carts/<int:cart_id>/items', methods=['POST'])
    @login_required
    def add_item(cart_id):
        if not db.check_cart(cart_id):
            abort(404)
        if not request.json or not 'product' in request.json or \
                not 'quantity' in request.json or request.json['product'] == "":
            abort(400)
        item = {
            'product': request.json['product'],
            'quantity': request.json['quantity'],
            'cart_id': cart_id
        }
        saved_item = db.save_item(item)
        if not saved_item:
            abort(400)
        return saved_item, 201

    @app.route('/online-store/api/carts/<int:cart_id>/items/<int:item_id>',
               methods=['DELETE'])
    @login_required
    def delete_item(cart_id, item_id):
        if not db.check_cart(cart_id):
            abort(404)
        deleted = db.remove_item(item_id)
        if deleted:
            return jsonify({'result': True})
        return jsonify({'error': 'Cart_item not found'}), 404

    @app.route('/online-store/api/register', methods=['POST'])
    def register():
        if current_user.is_authenticated:
            return jsonify({"error": "user is already authenticated"})
        if not request.json:
            return make_response(
                jsonify({'error': 'No data recieved'}),
                400
            )
        user = db.save_user(request.json)
        if not user:
            return make_response(
                jsonify({'error': 'Invalid data. Required "username", "email",'
                                  '"password".'}),
                400
            )
        return user

    @app.route('/online-store/api/login', methods=['POST'])
    def login():
        if (not request.json or not 'username' in request.json or
            not 'password' in request.json or request.json['username'] == "" or
            request.json['password'] == ""):
            return make_response(
                jsonify({'error': 'username or password is missed'}),
                400
            )

        user = db.User.get(db.User.username == request.json['username'])
        if not user or not user.check_password(request.json['password']):
            return jsonify({"error": "Invalid username or password"})

        login_user(user, remember=True)
        return jsonify({"success": f"user '{user.username}' successfully authenticated"})

    @app.route('/online-store/api/logout', methods=['GET'])
    @login_required
    def logout():
        logout_user()
        return jsonify({"success": " user successfully logout"})

if __name__ == '__main__':
    db.init_db()
    app = Flask(__name__)
    login_manage = LoginManager(app)
    #login_manage.login_view = 'login'
    app.config['SECRET_KEY'] = 'Vladik-Shokoladik ultra-sumer-mega-hiper-alfa-beta-extra-ordinary secret not a key'

    @login_manage.user_loader
    def load_user(id):
        return db.User.get(db.User.id == int(id))

    make_api(app)
    app.run(debug=True, host='0.0.0.0', port=5000)
