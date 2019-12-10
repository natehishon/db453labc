from datetime import datetime
from flaskDemo import db, login_manager
from flask_login import UserMixin

db.Model.metadata.reflect(db.engine)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    orders = db.relationship('Order', backref='userOrder', lazy=True)
    shopcarts = db.relationship('Shopcart', backref='userShopcart', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Order(db.Model):
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    orderLines = db.relationship('OrderLine', backref='orderOrderLine', lazy=True)

    def __repr__(self):
        return f"Order('{self.date_posted}')"

    def serialize(self):
        return {
            'id': self.id,
            'date_posted': self.date_posted,

        }


class OrderLine(db.Model):
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)

    def __repr__(self):
        return f"OrderLine('{self.date_posted}')"


class Shopcart(db.Model):
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    shopcartProds = db.relationship('ShopcartProd', backref='prodShopcart', lazy=True)

    def __repr__(self):
        return f"Shopcart('{self.date_posted}')"

    def serialize(self):
        return {
            'id': self.id,
            'date_posted': self.date_posted,

        }

class ShopcartProd(db.Model):
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    shopcart_id = db.Column(db.Integer, db.ForeignKey('shopcart.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)

    def __repr__(self):
        return f"ShopcartProd('{self.date_posted}')"

    def serialize(self):
        return {
            'id': self.id,
            'product_id': self.product_id,

        }

class Product(db.Model):
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    # orderLines = db.relationship('OrderLine', backref='product  OrderLine', lazy=True)


    def __repr__(self):
        return f"Product('{self.title}', '{self.date_posted}')"

    def serialize(self):
        return {
            'id': self.id,
            'title': self.title,

        }

