from application import db, login
from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(20))
    subtitle = db.Column(db.String(40))
    body = db.Column(db.String(280))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post {}>'.format(self.body)

class Member(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(20))
    subtitle = db.Column(db.String(40))
    body = db.Column(db.String(280))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Member {}'.format(self.body)

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    description = db.Column(db.String(280))

    def __repr__(self):
        return '<Category {}'.format(self.description)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    name = db.Column(db.String(20))
    description = db.Column(db.String(280))
    image = db.Column(db.String(80))
    stock = db.Column(db.Integer)
    price = db.Column(db.String(20))

    def __repr__(self):
        return '<Product {}'.format(self.description)

class Cart(db.Model):
    cart_id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class Checkout(db.Model):
    checkout_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    subtotal = db.Column(db.Float)
    product_id = db.Column(db.String(80))
    date = db.Column(db.String(80))
    total = db.Column(db.Float)