from flask import Blueprint, render_template


cookbp = Blueprint('cookbp', __name__)


@cookbp.route('/cook_ui')
def cook_ui():
    return render_template('cook_ui.html')


@cookbp.route('/cook_login')
def cook_login():
    return render_template('cook_login.html')


@cookbp.route('/view_order/<order_id>')
def view_order(order_id):
    return render_template('cook_view_order.html', order_id=order_id)