import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort, jsonify
from flaskDemo import app, db, bcrypt
import json
from flaskDemo.forms import RegistrationForm, LoginForm, UpdateAccountForm, AddToCartForm
from flaskDemo.models import User, Order, Product, OrderLine, Shopcart, ShopcartProd
from flask_login import login_user, current_user, logout_user, login_required
from datetime import datetime
from .__init__ import login_manager


@login_manager.user_loader
def load_user(id):
    return User.get(id)


@app.route("/")
@app.route("/home")
def home():

    results = Product.query.all()

    return render_template('products.html', title='Products', products=results)


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

    assign = ShopcartProd(product_id=pno, shopcart_id=shoppingCart.id)
    db.session.add(assign)
    db.session.commit()
    flash('Successfully add to cart!', 'success')

    return redirect(url_for('all_shopcarts'))


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
    results = Product.query.all()
    return render_template('products.html', title='Products', products=results)

# react
# @app.route("/products")
# def all_products():
#     results = Product.query.all()
#     return jsonify(results=[e.serialize() for e in results])


@app.route("/orders")
@login_required
def all_orders():
    results = Order.query.filter(Order.user_id == current_user.id)
    return render_template('orders.html', title='Orders', orders=results)


#react
# @app.route("/orders")
# def all_orders():
#     userid = 1
#     results = Order.query.filter(Order.user_id == userid)
#     return jsonify(orders=[e.serialize() for e in results])

@app.route("/order/<orderId>")
@login_required
def order(orderId):
    order1 = Order.query.filter(Order.user_id == current_user.id, Order.id == orderId).join(OrderLine,
                                                                                            Order.id == OrderLine.order_id) \
        .join(Product, Product.id == OrderLine.product_id).add_columns(Order.id, Product.title, Order.date_posted)

    return render_template('order.html', order=order1)


@app.route("/shopcart")
@login_required
def all_shopcarts():
    # results = Shopcart.query.filter(Shopcart.user_id == current_user.id, Shopcart.status=='active')

    exists = Shopcart.query.filter(Shopcart.user_id == current_user.id, Shopcart.status == "active").scalar()

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

    return render_template('shopcart.html', shopcartProds=shopcartProds, shoppingCart=shoppingCart)


#
# @app.route("/shopcart/<shopcartId>")
# @login_required
# def shopcart(shopcartId):
#
#     shoppingCart = Shopcart.query.get_or_404(shopcartId)
#
#     shopcartProds = Shopcart.query.filter(Shopcart.user_id == current_user.id, Shopcart.id == shopcartId).join(ShopcartProd, Shopcart.id == ShopcartProd.shopcart_id) \
#             .join(Product, Product.id == ShopcartProd.product_id).add_columns(Shopcart.id, Product.title, Shopcart.date_posted)
#
#
#
#     return render_template('shopcart.html', shopcartProds=shopcartProds, shoppingCart=shoppingCart)

# react
# @app.route("/products")
# def all_products():
#     results = Product.query.all()
#     # return render_template('dept_home.html', outString = results)
#     # posts = Post.query.all()
#     # return render_template('home.html', posts=posts)
#     # results2 = Faculty.query.join(Qualified,Faculty.facultyID == Qualified.facultyID) \
#     #            .add_columns(Faculty.facultyID, Faculty.facultyName, Qualified.Datequalified, Qualified.courseID) \
#     #            .join(Course, Course.courseID == Qualified.courseID).add_columns(Course.courseName)
#     # results = Faculty.query.join(Qualified,Faculty.facultyID == Qualified.facultyID) \
#     #           .add_columns(Faculty.facultyID, Faculty.facultyName, Qualified.Datequalified, Qualified.courseID)
#
#     return jsonify(results=[e.serialize() for e in results])


# @app.route("/about")
# def about():
#     return render_template('about.html', title='About')
#
#
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


#
#
# def save_picture(form_picture):
#     random_hex = secrets.token_hex(8)
#     _, f_ext = os.path.splitext(form_picture.filename)
#     picture_fn = random_hex + f_ext
#     picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)
#
#     output_size = (125, 125)
#     i = Image.open(form_picture)
#     i.thumbnail(output_size)
#     i.save(picture_path)
#
#     return picture_fn
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

#
#
# @app.route("/dept/new", methods=['GET', 'POST'])
# @login_required
# def new_dept():
#     form = DeptForm()
#     if form.validate_on_submit():
#         dept = Department(dname=form.dname.data, dnumber=form.dnumber.data,mgr_ssn=form.mgr_ssn.data,mgr_start=form.mgr_start.data)
#         db.session.add(dept)
#         db.session.commit()
#         flash('You have added a new department!', 'success')
#         return redirect(url_for('home'))
#     return render_template('create_dept.html', title='New Department',
#                            form=form, legend='New Department')
#
#

#
#
# @app.route("/dept/<dnumber>/update", methods=['GET', 'POST'])
# @login_required
# def update_dept(dnumber):
#     dept = Department.query.get_or_404(dnumber)
#     currentDept = dept.dname
#
#     form = DeptUpdateForm()
#     if form.validate_on_submit():          # notice we are are not passing the dnumber from the form
#         if currentDept !=form.dname.data:
#             dept.dname=form.dname.data
#         dept.mgr_ssn=form.mgr_ssn.data
#         dept.mgr_start=form.mgr_start.data
#         db.session.commit()
#         flash('Your department has been updated!', 'success')
#         return redirect(url_for('dept', dnumber=dnumber))
#     elif request.method == 'GET':
#         form.dnumber.data = dept.dnumber   # notice that we ARE passing the dnumber to the form
#         form.dname.data = dept.dname
#         form.mgr_ssn.data = dept.mgr_ssn
#         form.mgr_start.data = dept.mgr_start
#     return render_template('update_dept.html', title='Update Department',
#                            form=form, legend='Update Department')          # note the update template!
#
#
#

#
# @app.route("/dept/<dnumber>/delete", methods=['POST'])
# @login_required
# def delete_dept(dnumber):
#     dept = Department.query.get_or_404(dnumber)
#     db.session.delete(dept)
#     db.session.commit()
#     flash('The department has been deleted!', 'success')
#     return redirect(url_for('home'))
#
#
#
# # @app.route("/remove-employee-proj/delete", methods=['POST'])
# # @login_required
# # def delete_employee():
# #     req_data = request.get_json()
# #     print(req_data);
# #     # dept = Department.query.get_or_404(dnumber)
# #     # db.session.delete(dept)
# #     # db.session.commit()
# #     flash('The department has been deleted!', 'success')
# #     return redirect(url_for('home'))
#
#
#
#
# @app.route("/employees")
# def employees():
#     employeeProjects = Employee.query.join(Works_On, Employee.ssn == Works_On.essn) \
#         .add_columns(Employee.ssn, Employee.fname, Employee.lname, Works_On.essn, Works_On.pno) \
#         .join(Project, Project.pnumber == Works_On.pno).add_columns(Project.pname)
#
#     return render_template('assign_home.html', title='Employees', joined_m_n=employeeProjects)
#
# @app.route("/projects")
# def projects():
#     projects = Project.query.all()
#
#     return render_template('projects.html', title='Projects', joined_m_n=projects)
#
#
#
# @app.route("/assign1")
# @login_required
# def assign1():
#     essn = request.args.get('essn')
#     pno = request.args.get('pno')
#     assign = Works_On.query.get_or_404([essn,pno])
#     return render_template('assign.html', title=str(assign.essn)+"_"+str(assign.pno), assign=assign,now=datetime.utcnow())
#
#
# @app.route("/assign/<essn>/<pno>delete", methods=['POST'])
# @login_required
# def delete_assign(essn,pno):
#     assign = Works_On.query.get_or_404([essn,pno])
#     db.session.delete(assign)
#     db.session.commit()
#     flash('The works on has been deleted!', 'success')
#     return redirect(url_for('home'))
#
#
# @app.route("/project/<pnumber>")
# @login_required
# def project(pnumber):
#
#     project = Project.query.get_or_404(pnumber)
#
#     # project = sqlraw(select * from
#
#     currentEmployees = Employee.query.join(Works_On, Employee.ssn == Works_On.essn) \
#         .add_columns(Employee.ssn, Employee.fname, Employee.lname, Works_On.essn, Works_On.pno) \
#         .join(Project, Project.pnumber == Works_On.pno).add_columns(Project.pname).filter(Project.pnumber == pnumber)
#     #
#
#     currentIds = db.session.query(Employee.ssn). \
#         join(Works_On, Works_On.essn == Employee.ssn). \
#         filter(Works_On.pno == pnumber)
#
#     availableEmployees = Employee.query.filter(Employee.ssn.notin_(currentIds)).all()
#
#
#
#     return render_template('project.html', title=project.pname, project=project, employees=currentEmployees, currentIds = availableEmployees, now=datetime.utcnow())
#
#
# @app.route("/works/<essn>/<pno>works", methods=['GET'])
# @login_required
# def new_works(essn,pno):
#     new_works = Works_On(essn=essn, pno=pno, hours=0)
#     db.session.add(new_works)
#     db.session.commit()
#     return redirect(url_for('projects'))
