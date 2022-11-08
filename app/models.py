import datetime
from . import db


class User(db.Model):
    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True)
    registered_on = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow())
    fname = db.Column(db.String(20), nullable=False)
    lname = db.Column(db.String(20)) 
    email = db.Column(db.String(32))
    phone = db.Column(db.String(15), unique=True, nullable=False)
    orders = db.relationship('Orders', backref='user', lazy=True)


class Orders(db.Model):
    id = db.Column(db.INTEGER, primary_key=True)
    ordered_on = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow())
    order_data = db.Column(db.PickleType, nullable=True)
    ordered_by = db.Column(db.INTEGER, db.ForeignKey('user.id'), nullable=False)


class Categories(db.Model):
    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True)
    category_name = db.Column(db.String(20), nullable=False)
    orders = db.relationship('FoodItems', backref='categories', lazy=True)


class FoodItems(db.Model):
    id = db.Column(db.INTEGER, primary_key=True)
    added_on = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow())
    food_name = db.Column(db.String(20), nullable=False)
    food_description = db.Column(db.Text, nullable=False)
    food_img = db.Column(db.Text, nullable=False)
    food_price = db.Column(db.INTEGER, nullable=False)
    is_available = db.Column(db.Boolean, default=True)
    food_category = db.Column(db.INTEGER, db.ForeignKey('categories.id'), nullable=False)


# food review table
# admin table

# orders data table
'''
date -> primary_key
food_id -> foriegn key
ordered frequency
'''