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


@app.route('/passbooks', methods=['GET'])
def passbook_get_all():
    return dao.get_all_passbook()


@app.route('/api/passbooks/<int:passbook_id>', methods=['GET'])
def passbook_get_by_id(passbook_id):
    p = dao.get_passbook_by_id(passbook_id=passbook_id)
    return jsonify({
        "status": 200,
        "message": "successful",
        "data": {"customer_name": p.customer_name}
    })


# show list of passbook on passbook.html
@app.route("/user/passbook")
def passbook():
    passbook_type = dao.get_passbook_type()
    passbooks = dao.get_all_passbook()
    return render_template("user/passbook.html",
                           title="Sổ Tiết Kiệm", passbooks=passbooks, passbook_type=passbook_type)


@app.route("/user/passbook/charge", methods=['GET', 'POST'])
def passbook_charge():
    # if request.method == "POST":
    #     pass_id = request.form.get("charge_id_cus")
    #     pass_name = request.form.get("charge_name_cus")
    #     pass_money = request.form.get("charge_money_cus")
    #     update_passbook = (id = pass_id, customer_name = pass_name, )
    #     dao.add_passbook()
    return render_template("user/charge.html", title="Charge Pass")


@app.route("/user/passbook/add", methods=['GET', 'POST'])
def passbook_add_or_update():
    passbook_id = request.args.get("passbook_id")
    err = ""

    # customer_name = request.form.get("customer_name")
    # money = request.form.get("money")
    # address = request.form.get("address")
    # created_date = date.today()
    # phone = request.form.get("phone")
    # id_number = request.form.get("id_number")
    # passbook_type_id = request.form.get("passbook_type")
    #
    # new_passbook = Passbook(customer_name=customer_name, money=money, address=address, created_date=created_date,
    #                         phone=phone, id_number=id_number, passbook_type_id=passbook_type_id)

    if request.method == "POST":

        if passbook_id:  # Cap nhat
            data = dict(request.form.copy())
            data["passbook_id"] = passbook_id
            if dao.update_passbook(**data):
                return redirect(url_for("passbook"))
        else:  # Them
            data = dict(request.form.copy())
            if dao.add_passbook(**dict(request.form)):
                return redirect(url_for("passbook"))

        err = "Something wrong!!! Please back later!!!"

    passbook = None
    if passbook_id:
        passbook = dao.get_passbook_by_id(passbook_id=int(passbook_id))

    return render_template("user/passbook_add.html",
                           passbook_type=dao.get_passbook_type(),
                           passbook=passbook,
                           err=err)


@app.route("/api/passbooks/<int:passbook_id>", methods=["delete"])
def delete_passbook(passbook_id):
    if dao.delete_passbook(passbook_id=passbook_id):
        return jsonify({
            "status": 200,
            "message": "successful",
            "data": {"passbook_id": passbook_id}
        })

    return jsonify({
        "status": 500,
        "message": "Failed"
    })


@app.route("/user/rule")
def rule():
    rule = dao.get_all_passbook_type()
    return render_template("user/rule.html",
                           title="Quy Định", rule=rule)


@app.route("/api/passbooktype/<int:passbooktype_id>", methods=["delete"])
def delete_passbooktype(passbooktype_id):
    if dao.delete_rule(passbooktype_id=passbooktype_id):
        return jsonify({
            "status": 200,
            "message": "Successful",
            "data": {"passbooktype_id": passbooktype_id}
        })
    return jsonify({
        "status": 500,
        "message": "Failed",
    })


@app.route("/user/rule/add", methods=['GET', 'POST'])
def rule_add_or_update():
    passbooktype_id = request.args.get("passbooktype_id")
    err = ""
    if request.method == "POST":

        if passbooktype_id:  # Cap nhat
            data = dict(request.form.copy())
            data["passbooktype_id"] = passbooktype_id
            if dao.update_rule(**data):
                return redirect(url_for("rule"))
        else:  # Them
            data = dict(request.form.copy())
            if dao.add_rule(**dict(request.form)):
                return redirect(url_for("rule"))

        err = "Something wrong!!! Please back later!!!"

    rule = None
    if passbooktype_id:
        rule = dao.get_passbook_type_by_id(passbooktype_id=int(passbooktype_id))

    return render_template("user/rule_add.html",
                           rule=rule,
                           err=err)


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
