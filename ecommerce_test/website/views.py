from flask import Blueprint, render_template, request, flash, redirect, jsonify, url_for
from flask_login import login_required, current_user
from .models import Wishlist, Product, User, Cart
from . import db
import json
from email.mime.text import MIMEText
import smtplib

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])

def home():
    product = Product.query.filter().all()


    return render_template("home.html", user=current_user, PRODUCT=product)


@views.route('/delete-note', methods=['POST'])
def delete_note():
    wishlist = json.loads(request.data)
    wishlistId = wishlist['wishlistId']
    wishlist = Wishlist.query.get(wishlistId)
    if wishlist:
        if wishlist.user_id == current_user.id:
            db.session.delete(wishlist)
            db.session.commit()

    return jsonify({})


@views.route('/adminn', methods=['GET', 'POST'])

def admin():
    if request.method == 'POST':
        name = request.form.get('shoename')
        price = request.form.get('shoeprice')
        description = request.form.get('shoedescription')
        category = request.form.get('shoecategory')
        shoe_img = request.form.get('shoeimg')

        new_product = Product(name=name, price=price, desc=description, category=category, img_src=shoe_img)
        db.session.add(new_product)
        db.session.commit()
        

    return render_template("admin.html", user=current_user)

@views.route('/admin', methods=['GET', 'POST'])
def adminauth():
    if request.method == 'POST':
        username = request.form.get('email')
        password = request.form.get('password')

        if username == "batatirana":
            if password == "tirana17":
                return redirect("/adminn")
        else:
            pass
    return render_template("adminlogin.html", user=current_user)


@views.route('/product/<id>')
def product_page(id):
    product = Product.query.filter(id==Product.id).first()

    return render_template("productinfo.html", PRODUCT=product, user=current_user)




@views.route('/add_to_wishlist', methods = ['POST'])
def add_to_wishlist():
    user_id = current_user.id
    product_id = request.form['product_id']
    name = request.form['name']
    price = request.form['price']
    category = request.form['category']
    new_item = Wishlist(user_id=user_id, id=product_id, name=name, price=price, category=category)
    db.session.add(new_item)
    db.session.commit()
   

    return redirect('/wishlist')

@views.route('/wishlist', methods=['GET','POST'])
@login_required
def wishlist():
    product = Wishlist.query.filter_by(user_id=current_user.id).all()
    return render_template('wishlist.html', PRODUCT=product, user=current_user)
    
@views.route('/delete_item/<int:item_id>')
@login_required
def delete_item(item_id):
    item = Wishlist.query.filter_by(id=item_id).first()
    db.session.delete(item)
    db.session.commit()
    return redirect(url_for('views.wishlist'))

@views.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    product = Product.id
    if request.method == 'POST':
        name = request.form['name']
        address = request.form['address']
        city = request.form['city']
        email = current_user.email
        phonenumber = request.form['number']
        size = request.form['size']
        items = Cart.query.filter_by(user_id=current_user.id).all()
        items = [item.name for item in items]
        send_email_notification(name, address, city, email, items, size, phonenumber)
        flash('Your order has been placed successfully!')
        return redirect(url_for('views.home'))
    return render_template("checkout.html", user=current_user, PRODUCT=product)

def send_email_notification(name, address, city, email, items, size, phonenumber):
    gmail_user = 'desh.corporation1@gmail.com'
    gmail_password = 'lwvudcbkpvienjxx'

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login(gmail_user, gmail_password)
        message = 'Name: {}\nAddress: {}\nEmail: {}\nCity: {}\nItems: {}\nSize: {}\nPhone number: {}'.format(name, address, email, city, items, size, phonenumber)
        msg = MIMEText(message)
        msg['Subject'] = 'New Order'
        msg['From'] = gmail_user
        msg['To'] = gmail_user
        server.send_message(msg)
        server.quit()
    except Exception as e:
        print(e)

@views.route('/delete', methods = ['GET', 'POST'])
def delete():
    
    product = Product.query.filter_by(id=3).first()
    db.session.delete(product)
    db.session.commit()
    
        
    


    return "success"

@views.route('/add_to_cart', methods = ['POST'])
def add_to_cart():
    user_id = current_user.id
    product_id = request.form['productid']
    name = request.form['namee']
    price = request.form['pricee']
    category = request.form['categoryy']
    new_item = Cart(user_id=user_id, id=product_id, name=name, price=price, category=category)
    db.session.add(new_item)
    db.session.commit()
   

    return redirect('/cart')

@views.route('/cart', methods=['GET','POST'])
@login_required
def cart():
    product = Cart.query.filter_by(user_id=current_user.id).all()
    return render_template('cart.html', PRODUCT=product, user=current_user)
    
@views.route('/delete_cart/<int:item_id>')
@login_required
def delete_cart(item_id):
    item = Cart.query.filter_by(id=item_id).first()
    db.session.delete(item)
    db.session.commit()
    return redirect(url_for('views.cart'))


