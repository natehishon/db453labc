import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort, jsonify
from flaskDemo import app, db, bcrypt
from flaskDemo.forms import RegistrationForm, LoginForm, UpdateAccountForm
from flaskDemo.models import User, Order, Product, OrderLine, Shopcart, ShopcartProd
from flask_login import login_user, current_user, logout_user, login_required
from .__init__ import login_manager
from sqlalchemy import text




@login_manager.user_loader
def load_user(id):
    return User.get(id)


@app.route("/")
@app.route("/home")
def home():
    cmd = 'select * from Product'
    results = db.session.execute(text(cmd))
    count = 'select count(*) from Product as count'
    countResults = db.session.execute(text(count))



    return render_template('products.html', title='Products', products=results, count=countResults.first()[0])


@app.route("/remove-from-cart")
@login_required
def removeFromCart():
    pno = request.args.get('pno')
    ShopcartProd.query.filter(ShopcartProd.id == pno).delete()
    db.session.commit()
    flash('Successfully removed from cart!', 'success')
    return redirect(url_for('all_shopcarts'))


@app.route("/add-to-cart")
@login_required
def addToCart():
    pno = request.args.get('pno')

    exists = Shopcart.query.filter(Shopcart.user_id == current_user.id, Shopcart.status == "active").scalar()

    if exists == None:
        shoppingCart = Shopcart(user_id=current_user.id, status='active')
        db.session.add(shoppingCart)
        db.session.commit()
    else:
        shoppingCart = Shopcart.query.filter(Shopcart.user_id == current_user.id, Shopcart.status == "active").first()

    shopProdExist = ShopcartProd.query.filter(ShopcartProd.product_id == pno,
                                              ShopcartProd.shopcart_id == shoppingCart.id).scalar()

    if shopProdExist == None:
        assign = ShopcartProd(product_id=pno, shopcart_id=shoppingCart.id)
        db.session.add(assign)
        db.session.commit()
        flash('Successfully added to cart', 'success')
    else:
        flash('Already in cart', 'danger')

    return redirect(url_for('home'))


@app.route("/checkout")
@login_required
def checkout():
    shopcartID = request.args.get('shopcartId')

    shoppingCart = Shopcart.query.get_or_404(shopcartID)

    shopcartProds = Shopcart.query.filter(Shopcart.user_id == current_user.id, Shopcart.id == shoppingCart.id).join(
        ShopcartProd, Shopcart.id == ShopcartProd.shopcart_id) \
        .join(Product, Product.id == ShopcartProd.product_id).add_columns(Product.title,
                                                                          Shopcart.date_posted, Product.id)
    newOrder = Order(user_id=current_user.id)
    db.session.add(newOrder)
    db.session.commit()

    for shopProd in shopcartProds:
        assign = OrderLine(product_id=shopProd.id, order_id=newOrder.id)
        db.session.add(assign)
        db.session.commit()

    shoppingCart.status = "paid"
    db.session.add(shoppingCart)
    db.session.commit()

    flash('Successfully checked out', 'success')
    return redirect(url_for('home'))


#
@app.route("/products")
def all_products():

    cmd = 'select * from Product'
    result = db.session.execute(text(cmd))


    return render_template('products.html', title='Products', products=result)

@app.route("/general-sub")
def general_sub():

    cmd = 'select * from ShopCart where status in (select distinct status from ShopCart)'
    result = db.session.execute(text(cmd))


    return render_template('general.html', title='General', results=result)

@app.route("/general-compound")
def general_compound():

    # ORDER IS RESERVED
    sql = text("SELECT * FROM ShopCart WHERE user_id = 1 and status = 'active'")
    result = db.engine.execute(sql)


    return render_template('general.html', title='General', results=result)


@app.route("/general-join")
def general_join():

    # ORDER IS RESERVED
    sql = text("SELECT ShopCart.id, shopcart_prod.id from ShopCart JOIN shopcart_prod on ShopCart.id = shopcart_prod.shopcart_id")
    result = db.engine.execute(sql)


    return render_template('general.html', title='General', results=result)



# react
@app.route("/react-products")
def react_products():
    results = Product.query.all()
    return jsonify(results=[e.serialize() for e in results])


@app.route("/orders")
@login_required
def all_orders():
    results = Order.query.filter(Order.user_id == current_user.id)
    return render_template('orders.html', title='Orders', orders=results)


# react
@app.route("/react-orders")
def react_orders():
    userid = 1
    results = Order.query.filter(Order.user_id == userid)
    return jsonify(orders=[e.serialize() for e in results])

@app.route("/order/<orderId>")
@login_required
def order(orderId):
    order = Order.query.filter(Order.id == orderId).first()
    orderProds = Order.query.filter(Order.user_id == current_user.id, Order.id == orderId).\
        join(OrderLine, Order.id == OrderLine.order_id)\
        .join(Product, Product.id == OrderLine.product_id).add_columns(Order.id, Product.title, Order.date_posted)

    return render_template('order.html', orderProds=orderProds, order=order)


@app.route("/shopcart")
@login_required
def all_shopcarts():
    exists = Shopcart.query.filter(Shopcart.user_id == current_user.id, Shopcart.status == "active").scalar()

    count = 0


    if exists == None:

        shoppingCart = Shopcart(user_id=current_user.id, status='active')
        shopcartProds = []
        db.session.add(shoppingCart)
        db.session.commit()
    else:

        shoppingCart = Shopcart.query.filter(Shopcart.user_id == current_user.id, Shopcart.status == "active").first()
        shopcartProds = Shopcart.query.filter(shoppingCart.user_id == current_user.id,
                                              Shopcart.id == shoppingCart.id).join(ShopcartProd,
                                                                                   Shopcart.id == ShopcartProd.shopcart_id) \
            .join(Product, Product.id == ShopcartProd.product_id).add_columns(ShopcartProd.id, Product.title,
                                                                              Shopcart.date_posted)
        count = shopcartProds.count()



    return render_template('shopcart.html', shopcartProds=shopcartProds, shoppingCart=shoppingCart, count=count)


@app.route("/react-shopcart")
@login_required
def react_cart():

    count = 0
    userid = 1

    exists = Shopcart.query.filter(Shopcart.user_id == userid, Shopcart.status == "active").scalar()

    if exists == None:

        shoppingCart = Shopcart(user_id=userid, status='active')
        shopcartProds = []
        db.session.add(shoppingCart)
        db.session.commit()
    else:

        shoppingCart = Shopcart.query.filter(Shopcart.user_id == userid, Shopcart.status == "active").first()
        shopcartProds = Shopcart.query.filter(shoppingCart.user_id == userid,
                                              Shopcart.id == shoppingCart.id).join(ShopcartProd,
                                                                                   Shopcart.id == ShopcartProd.shopcart_id) \
            .join(Product, Product.id == ShopcartProd.product_id).add_columns(ShopcartProd.id, Product.title,
                                                                              Shopcart.date_posted)
        count = shopcartProds.count()

    return jsonify(shopcartProds=[e.serialize() for e in shopcartProds], shoppingCart=shoppingCart.serialize())


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/add_product', methods=['POST'])
def add_posts():
    content = request.get_json()
    print(content)
    product = Product(title=content['title'])
    db.session.add(product)
    db.session.commit()

    resp = jsonify(success=True)
    return resp

#
#
@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


#

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


#

@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account',
                           image_file=image_file, form=form)
