from datetime import datetime
from flaskDemo import db, login_manager
from flask_login import UserMixin
from functools import partial
from sqlalchemy import orm

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

#
# class Post(db.Model):
#      __table_args__ = {'extend_existing': True}
#      id = db.Column(db.Integer, primary_key=True)
#      title = db.Column(db.String(100), nullable=False)
#      date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
#      content = db.Column(db.Text, nullable=False)
#      user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
#
#      def __repr__(self):
#          return f"Post('{self.title}', '{self.date_posted}')"


class Order(db.Model):
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    # title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    # content = db.Column(db.Text, nullable=False)
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
    # title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    # content = db.Column(db.Text, nullable=False)
    # user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)

    def __repr__(self):
        return f"OrderLine('{self.date_posted}')"


class Shopcart(db.Model):
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    # content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    shopcartProds = db.relationship('ShopcartProd', backref='prodShopcart', lazy=True)

    def __repr__(self):
        return f"Shopcart('{self.date_posted}')"

class ShopcartProd(db.Model):
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    # title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    # content = db.Column(db.Text, nullable=False)
    # user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    shopcart_id = db.Column(db.Integer, db.ForeignKey('shopcart.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)

    def __repr__(self):
        return f"ShopcartProd('{self.date_posted}')"

class Product(db.Model):
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    # content = db.Column(db.Text, nullable=False)
    orderLines = db.relationship('OrderLine', backref='product  OrderLine', lazy=True)


    def __repr__(self):
        return f"Product('{self.title}', '{self.date_posted}')"

    def serialize(self):
        return {
            'id': self.id,
            'title': self.title,

        }

# orderline





#
#
# class Dependent(db.Model):
#     __table__ = db.Model.metadata.tables['dependent']
#
# class Department(db.Model):
#     __table__ = db.Model.metadata.tables['department']
#
# # used for query_factory
# def getDepartment(columns=None):
#     u = Department.query
#     if columns:
#         u = u.options(orm.load_only(*columns))
#     return u
#
# def getDepartmentFactory(columns=None):
#     return partial(getDepartment, columns=columns)
#
# class Dept_Locations(db.Model):
#     __table__ = db.Model.metadata.tables['dept_locations']
#
# class Employee(db.Model):
#     __table__ = db.Model.metadata.tables['employee']
# class Project(db.Model):
#     __table__ = db.Model.metadata.tables['project']
# class Works_On(db.Model):
#     __table__ = db.Model.metadata.tables['works_on']

    

  
