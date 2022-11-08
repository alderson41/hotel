from flask import Blueprint, render_template


adminbp = Blueprint('adminbp', __name__)


@adminbp.route('/admin')
def admin():
    return render_template('admin.html')