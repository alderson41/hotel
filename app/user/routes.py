from flask import Blueprint, render_template, request, jsonify, session
from .. import socketio, db, emit, join_room
from ..models import *
import json


user = Blueprint('user',__name__)


@user.app_template_filter('to_string')
def to_string(value):
    return json.dumps(value)


@user.route('/set_table/<table_id>')
def set_table(table_id):
    return render_template('create_table.html')


@user.route('/create_table', methods=['POST'])
def create_table():
    data = request.get_json(force=True)
    user = User.query.filter_by(phone=data['phone']).first()
    session['user'] = data['phone']
    if not user:
        new_user = User(fname=data['fname'],lname=data['lname'],email=data['email'],phone=data['phone'])
        db.session.add(new_user)
        db.session.commit()
    return jsonify(resp='ok')


@user.route('/')
def index():
    categories = Categories.query.all()
    # query only new and popular foods 4 in each row
    return render_template('index.html', categories=categories)


@user.route('/cart')
def cart():
    categories = Categories.query.all()
    return render_template('cart.html', categories=categories)


@user.route('/history')
def history():
    categories = Categories.query.all()
    orders = Orders.query.order_by(Orders.ordered_on.desc()).filter_by(ordered_by=session['user']).all()
    return render_template('account_history.html', categories=categories, orders=orders)


@user.route('/order_details/<order_id>')
def order_details(order_id):
    order = Orders.query.filter_by(id=order_id).first()
    return render_template('order_details.html', order=order)


@user.route('/orders')
def orders():
    # view current session orders
    return render_template('orders.html')


@user.route('/error')
def error():
    # render this when user hasnt scanned the qr instead used direct url for other routes without setting table
    return render_template('error.html')


@socketio.on('join')
def on_join(data):
    join_room(data['table_id'])


@socketio.on('update')
def new_order(data):
    # commit to db after  the cook sets the status as completed. till then store in localstorage
    order_id = data['order_id']
    ordered_by = data['identifier']
    new_order = Orders(id=order_id, order_data=data, ordered_by=ordered_by)
    db.session.add(new_order)
    db.session.commit()
    print('order received')
    emit('ord_updates', data, broadcast=True)


@socketio.on('order received')
def order_received(data):
    emit('order update', "Order has been received", to=data['table_id'])


@socketio.on('foodstatus')
def food_status(data):
    print(data)
    emit('foodupdate', data, to=data['table_id'])