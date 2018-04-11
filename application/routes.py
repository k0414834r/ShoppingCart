from application import app, db
from application.models import User, Post, Member, Product, Cart
from flask import render_template, url_for, redirect, flash
from application.forms import LoginForm, RegistrationForm
from flask_login import logout_user, login_user, current_user

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
