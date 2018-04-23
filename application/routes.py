from application import app, db
from application.models import User, Post, Member, Product, Cart, Checkout
from flask import render_template, url_for, redirect, flash, request
from application.forms import LoginForm, RegistrationForm
from flask_login import logout_user, login_user, current_user
from datetime import datetime

@app.route("/")
@app.route('/index')
def index():
    posts = Post.query.all()
    member = Member.query.all()
    return render_template('index.html', posts=posts, member=member, title="Welcome!")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}; "Remember me" is {}'.format(form.username.data, form.remember_me.data), 'flash')
        user = User.query.filter_by(username=form.username.data).first()

        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password', 'flash')
            return redirect(url_for('login'))

        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('login'))
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return "You have been registered"

    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!', 'flash')
        return redirect(url_for('login'))

    return render_template('register.html', title='Register', form=form)

@app.route('/weather')
def weather():
    return render_template('weather.html')

@app.route('/products')
def product():
    products = Product.query.all()

    return render_template('products.html', products=products)

@app.route('/product/<int:product_id>')
def products(product_id):
    product_data = Product.query.filter_by(id=product_id).first()
    return render_template('details.html', data=product_data)

@app.route('/cart')
def cart():
    if current_user.is_anonymous:
        return redirect(url_for('login'))

    products_in_cart = Cart.query.filter_by(user_id=current_user.id).join(Product, Cart.product_id == Product.id).add_columns(Product.name, Product.price, Product.image, Product.id).all()
    return render_template('cart.html', products=products_in_cart)

@app.route('/addToCart/<int:product_id>/<string:from_page>')
def addToCart(product_id, from_page):
    if current_user.is_anonymous:
        return redirect(url_for('login'))

    cart = Cart(user_id=current_user.id, product_id=product_id)
    db.session.add(cart)
    db.session.commit()
    return redirect(url_for('cart'))

@app.route('/removeFromCart/<int:product_id>/<string:from_page>')
def removeFromCart(product_id, from_page):
    if current_user.is_anonymous:
        return redirect(url_for('login'))

    cart = Cart.query.filter_by(user_id=current_user.id, product_id=product_id).first()
    db.session.delete(cart)
    db.session.commit()
    return redirect(url_for('cart'))

@app.route('/removeFromCheckout/<int:product_id>/<string:from_page>')
def removeFromCheckout(product_id, from_page):
    if current_user.is_anonymous:
        return redirect(url_for('login'))

    cart = Cart.query.filter_by(user_id=current_user.id, product_id=product_id).first()
    db.session.delete(cart)
    db.session.commit()
    return redirect(url_for('checkout'))

@app.route('/checkout')
def checkout():
    if current_user.is_anonymous:
        return redirect(url_for('login'))

    products_in_cart = Cart.query.filter_by(user_id=current_user.id).join(Product, Cart.product_id == Product.id).add_columns(Product.name, Product.price, Product.image, Product.id).all()

    sum = 0
    for row in products_in_cart:
        sum += row.price

    productNum = Cart.query.filter_by(user_id=current_user.id).count()

    return render_template('checkout.html', products_in_cart=products_in_cart, productNum=productNum, sum=sum)

@app.route('/submissions', methods=['POST'])
def submissions(checkout_id, subtotal, product_id, date, total):
    #get submit bill info
    cardname = request.form.get('cardname')
    cardnumber = request.form.get('cardnumber')

    #gather cart items
    products_in_cart = Cart.query.filter_by(user_id=current_user.id).join(Product,Cart.product_id == Product.id).add_columns(Product.name, Product.price, Product.image, Product.id).all()

    #create a checkout submit record and put it to the db
    receipt = Checkout(checkout_id=checkout_id, user_id=current_user.id, subtotal=subtotal, product_id=product_id, date=date, total=total)
    date = datetime.now()
    subtotal = sum
    total = subtotal * 0.95
    product_id = products_in_cart.Product.id
    db.session.add(receipt)
    db.session.commit()

    flash("checkout_action:" + " " + cardname + " " + cardnumber + "subtotal: " + subtotal + "total " + total)
    return render_template('submissions.html', product_id=product_id, date=date, subtotal=subtotal, total=total, checkout_id=checkout_id, cardname=cardname, cardnumber=cardnumber)