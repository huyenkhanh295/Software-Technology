import csv
from _datetime import datetime
import os
import pyexcel as pe
from io import StringIO

from flask import render_template, redirect, request, url_for, flash, jsonify, make_response, send_from_directory, \
    send_file
from flask_login import login_user, login_required
from flask_swagger_ui import get_swaggerui_blueprint
from wtforms.ext import dateutil

from app import dao, utils
from app import app, login
from app.forms import LogInForm
from app.models import *
import hashlib


# @app.route('/static/<path:path>')
# def send_static(path):
#     return send_from_directory('static', path)
#
#
# SWAGGER_URL = '/swagger'
# API_URL = '/static/swagger.json'
# swaggerui_blueprint = get_swaggerui_blueprint(
#     SWAGGER_URL,
#     API_URL,
#     config={
#         'app_name': 'Kiểm Thử Api'
#     }
# )
# app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)
#

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
    kw = request.args.get("keyword")
    id = request.args.get("id")

    passbook_type = dao.get_passbook_type()
    passbooks = dao.get_passbook(id=id, keyword=kw)

    return render_template("user/passbook.html",
                           title="Sổ Tiết Kiệm", passbooks=passbooks, passbook_type=passbook_type)


@app.route("/user/passbook/add", methods=['GET', 'POST'])
def passbook_add_or_update():
    passbook_id = request.args.get("passbook_id")
    err = ""

    if request.method == "POST":

        if passbook_id:  # Cap nhat
            data = dict(request.form.copy())
            data["passbook_id"] = passbook_id
            if dao.update_passbook(**data):
                return redirect(url_for("passbook"))
        else:  # Them
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


# show list of deposit slip on receipt.html
@app.route("/user/deposit_slip")
def deposit_slip_list():
    deposit_slip = dao.get_deposit_slip()

    return render_template("user/receipt.html",
                           title="Phiếu gửi tiền", deposit_slip=deposit_slip, creator=dao.get_user())


@app.route("/user/withdrawal_slip")
def withdrawal_slip_list():
    withdrawal_slip = dao.get_withdrawal_slip()

    return render_template("user/receipt.html",
                           title="Phiếu rut tien", withdrawal_slip=withdrawal_slip, creator=dao.get_user())


@app.route("/user/deposit_slip/add", methods=['GET', 'POST'])
def make_a_deposit_slip():
    err = ''
    id = request.args.get("id")
    p = dao.get_passbook_by_id(passbook_id=id)
    if id:
        # neu ma so hop le
        if p:
            if p.passbook_type_id != 1:
                err = 'Loai tiet kiem khong hop le! Phai thuoc loai khong thoi han'
        else:
            err = 'Ma so khong hop le'

    if request.method == "POST":
        if dao.add_deposit_slip(p.id, p.customer_name, **dict(request.form)):
            err = 'Lap phieu gui tien thanh cong'
            return redirect(url_for("deposit_slip_list"))

    return render_template("user/receipt_add.html", creator=dao.get_user(),
                           err=err, passbook=p, deposit_slip=dao.get_deposit_slip())


@app.route("/user/withdrawal_slip/add", methods=['GET', 'POST'])
def make_a_withdrawal_slip():
    err = ''
    id = request.args.get("id")
    p = dao.get_passbook_by_id(passbook_id=id)
    if id:
        # neu ma so hop le
        if p:
            if (datetime.datetime.now() - p.created_date).days >= 15:
                # loai so ko ky han
                if p.passbook_type_id == 1:
                    withdrawal_money = request.args.get("money")
                    if withdrawal_money:
                        # kiem tra so du
                        if float(withdrawal_money) <= p.money:
                            if request.method == "POST":
                                if dao.add_withdrawal_slip(**dict(request.form)):
                                    err = 'Lap phieu rut tien thanh cong'
                                    return redirect(url_for("withdrawal_slip_list"))
                        else:
                            err = 'So du khong du'
                # loai so co ki han
                else:
                    pass
            else:
                err = 'Chua den ngay duoc phep rut tien (it nhat la 15 ngay)'
        else:
            err = 'Ma so khong hop le'

    return render_template("user/receipt_add.html", creator=dao.get_user(),
                           err=err, withdrawal_slip=dao.get_withdrawal_slip())


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


@app.route("/user/report")
def report():
    return render_template("user/report.html", title='Báo cáo')


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


@app.route("/user/report/month", methods=["post", "get"])
def report_month():
    render_template("user/report-month.html")
    if request.method == "POST":
        month = request.form.get("report_month")
        year = request.form.get("report_year")
        start = year + "-0" + month + "-" + "01" + " 00:00:00"
        end = year + "-0" + month + "-" + "29" + " 00:00:00"
        flash(f'kết thúc {end}')
        flash(f'bắt đầu {start}')
        recedata = Receipt.query.filter(Receipt.created_date <= end).filter(Receipt.created_date >= start)
        data = Passbook.query.filter(Passbook.created_date <= end).filter(Passbook.created_date >= start)
        print(data)
        print(recedata)
        return render_template("user/report-month.html", title='Báo cáo theo tháng', datas=data, data2=recedata)
    else:
        return render_template("user/report-month.html", title='Báo cáo theo tháng')


@app.route("/user/report/day", methods=["post", "get"])
def report_day():
    if request.method == "POST":
        date = request.form.get("report_date_from")
        start = date + " 00:00:00"
        end = date + " 23:10:10"
        # end = request.form.get("report_date_to")
        flash(f'kết thúc {end}')
        flash(f'bắt đầu {start}')
        recedata = Receipt.query.filter(Receipt.created_date <= end).filter(Receipt.created_date >= start)
        data = Passbook.query.filter(Passbook.created_date <= end).filter(Passbook.created_date >= start)
        # db.session.query(Passbook).filter_by().first()
        print(data)
        print(recedata)
        # with open('dump.csv', 'wb') as f:
        #     out = csv.writer(f)
        #     # out.writerow(['id', 'customer_name', 'address', 'created_date', 'money', 'phone','id_number', W'passbook_type_id', 'active'])
        #     for item in data:
        #         out.writerow([item.id, item.customer_name, item.address, item.created_date, item.money, item.phone,item.id_number, item.passbook_type_id, item.active])
        # if data:
        #     result = []
        #     for what in data:
        #         all = what.id + ',' + what.customer_name + ',' + what.address + ',' + what.created_date
        #         + ',' + what.money + ',' + what.phone + ',' + what.id_number + ','
        #         + what.passbook_type_id + ',' + what.active
        #         result.append([all])
        #     si = StringIO()
        #     cw = csv.writer(si)
        #     cw.writerows(result)
        #     output = make_response(si.getvalue())
        #     output.headers["Content-Disposition"] = "attachment; filename=export.csv"
        #     output.headers["Content-type"] = "text/csv"
        #     return output
        # if data:
        #     return send_file(utils.export_csv(ok))
        return render_template("user/report-day.html", title='Báo cáo theo ngày', datas=data, data2=recedata)
    else:
        return render_template("user/report-day.html", title='Báo cáo theo ngày')


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
