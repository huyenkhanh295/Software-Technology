from datetime import date

from flask import render_template, redirect, request, url_for, flash, jsonify, make_response, send_from_directory
from flask_login import login_user, login_required
from flask_swagger_ui import get_swaggerui_blueprint
from app import dao
from app import app, login
from app.forms import LogInForm
from app.models import *
import hashlib


@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)


SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': 'Kiểm Thử Api'
    }
)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)


# posts = [
#     {
#         'author': 'Cor',
#         'title': 'blog',
#         'content': 'first',
#         'date_posted': 'april'
#     },
#     {
#         'author': 'Corqwe',
#         'title': 'blogasdas',
#         'content': 'firdasdasst',
#         'date_posted': 'aprdasdasdil'
#     }
# ]


@app.route("/")
def index():
    return render_template("index.html")


# @app.route("/passbooks", methods=["GET"])
# def get_passbooks():
#     return Passbook.query.all()
#
#
# @app.route("/passbooks/<int:passbook_id>", methods=["GET"])
# def get_passbooks_by_id(passbook_id):
#     pass
#
#
# @app.route("/passbooks/add", methods=["POST"])
# def insert_passbooks():
#     pass

@app.route('/passbooks', methods=['GET'])
def passbook_get():
    return dao.get_all_passbook()


@app.route('/passbooks/<id>', methods=['GET'])
def passbook_get_id():
    return dao.get_id_passbook()


@app.route("/user/openpassbook")
def openpassbook():
    pass_role = dao.get_passbook_role()
    passbooks = dao.get_all_passbook()
    return render_template("user/openpassbook.html", title="Open Pass", passbooks=passbooks, pass_role=pass_role)


@app.route("/user/openpassbookupdate")
def openpassbookupdate():
    return render_template("user/openpassbook.html", title="Update Pass")


@app.route("/user/openpassbook/charge", method=['GET','POST'])
def openpassbook_charge():
    # if request.method == "POST":
    #     pass_id = request.form.get("charge_id_cus")
    #     pass_name = request.form.get("charge_name_cus")
    #     pass_money = request.form.get("charge_money_cus")
    #     update_passbook = (id = pass_id, customer_name = pass_name, )
    #     dao.add_passbook()
    return render_template("user/charge.html", title="Charge Pass")


@app.route("/user/openpassbook/add", methods=['GET', 'POST'])
def openpassbook_add():
    name_cus = request.form.get("name_cus")
    money_cus = request.form.get("money_cus")
    address = request.form.get("address_cus")
    time = date.today()
    phone = request.form.get("mobile_cus")
    cmnd = request.form.get("cmnd_cus")
    role = request.form.get("role")

    new_passbook = Passbook(customer_name=name_cus, address=address, date_create=time, money=money_cus,
                            phone_number=phone, id_number=cmnd, passbook_role_id=role)

    if request.method == "POST":
        dao.add_passbook(new_passbook)
        flash(f'Chào mừng !', 'success')
    else:
        flash(f'Chào mừng ', 'failed')
    return render_template("user/openpassbookadd.html", title="Add Pass")


# @app.route("/user/sendpassbook/", methods=['GET','POST'])
# def sendpassbook():
#


# @app.route('/passbooks', methods=['POST'])
# def passbook_post():
#     return dao.add_passbook()


@app.route('/passbooks/<id>', methods=['PUT'])
def passbook_update_by_id(id):
    data = request.get_json()
    get_passbook = Passbook.query.get(id)
    if data.get('customer_name'):
        get_passbook.customer_name = data['customer_name']
    if data.get('address'):
        get_passbook.address = data['address']
    if data.get('date_create'):
        get_passbook.date_create = data['date_create']
    if data.get('money'):
        get_passbook.money = data['money']
    if data.get('phone_number'):
        get_passbook.phone_number = data['phone_number']
    if data.get('id_number'):
        get_passbook.id_number = data['id_number']
    if data.get('passbook_role_id'):
        get_passbook.passbook_role_id = data['passbook_role_id']
    db.session.add(get_passbook)
    db.session.commit()
    passbook_schema = PassBookSchema(
        only=['id', 'customer_name', 'address', 'date_create', 'money', 'phone_number', 'id_number',
              'passbook_role_id'])
    passbook = passbook_schema.dump(get_passbook)
    return make_response(jsonify({"passbook": passbook}))


@app.route('/passbooks/<id>', methods=['DELETE'])
def passbook_delete_by_id(id):
    get_passbook = Passbook.query.get(id)
    db.session.delete(get_passbook)
    db.session.commit()
    return make_response("", 204)


@app.route("/login-user", methods=["post", "get"])
def login_user_on():
    if current_user.is_authenticated:
        return redirect(url_for('user'))
    form = LogInForm()
    if form.validate_on_submit():
        password = str(hashlib.md5(form.password.data.strip().encode("utf-8")).hexdigest())
        username = form.username.data
        user = User.query.filter(User.username == username.strip(),
                                 User.password == password).first()
        password = User.query.filter
        if user and password:
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash(f'Chào mừng {form.username.data}!', 'success')
            return redirect(next_page) if next_page else redirect(url_for('user'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template("user/login.html", title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('user'))


@app.route("/user")
def user():
    return render_template("user/index.html")


@app.route("/term")
def term():
    return render_template("user/term.html")


#
# @app.route("/user")
# def user():
#     return render_template("user/index.html")


@app.route("/login-admin", methods=["post", "get"])
def login_admin():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password", "")
        password = str(hashlib.md5(password.strip().encode("utf-8")).hexdigest())
        user = User.query.filter(User.username == username.strip(),
                                 User.password == password).first()
        if user:
            login_user(user=user)
            return redirect("/admin")
        else:
            return render_template("admin/login-failed.html")
    return redirect("/admin")


@login.user_loader
def user_load(user_id):
    return User.query.get(user_id)


if __name__ == "__main__":
    app.run(debug=True)
