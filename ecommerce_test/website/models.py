from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class Wishlist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    name = db.Column(db.String(10000))
    price = db.Column(db.Integer)
    category = db.Column(db.String)
    date = db.Column(db.DateTime(timezone=True), default=func.now())

class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    name = db.Column(db.String(10000))
    price = db.Column(db.Integer)
    category = db.Column(db.String)
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    wishlist = db.relationship('Wishlist')


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    price = db.Column(db.Integer)
    desc = db.Column(db.String(200))
    category = db.Column(db.String)
    img_src = db.Column(db.String)


    