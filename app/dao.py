import datetime

from flask import request, make_response, jsonify

from app.models import *


# Swagger
# def add_passbook():
#     data = request.get_json()
#     passbook_schema = PassBookSchema()
#     passbooks = passbook_schema.load(data)
#     result = passbook_schema.dump(passbooks.create())
#     return make_response(jsonify({"passbook": result}), 200)


# Swagger
# def get_all_passbook():
#     get_passbook = Passbook.query.all()
#     passbook_schema = PassBookSchema(many=True)
#     passbooks = passbook_schema.dump(get_passbook)
#     return make_response(jsonify({"passbook": passbooks}))

# passbook
def get_passbook_by_id(passbook_id):
    return Passbook.query.get(passbook_id)


def get_passbook(id=None, keyword=None):
    p = Passbook.query

    if keyword:
        p = p.filter(Passbook.customer_name.contains(keyword))
    if id:
        p = p.filter(Passbook.id == id)

    return p.all()


def get_passbook_type():
    return PassbookType.query.all()


def add_passbook(customer_name, address, id_number, phone, money, passbook_type_id, active=None):
    p = Passbook()
    p.customer_name = customer_name
    p.address = address
    p.id_number = id_number
    p.phone = phone
    p.created_date = datetime.datetime.now()
    p.money = float(money)
    p.passbook_type_id = passbook_type_id
    if active:
        active = 'True'
    else:
        active = ''
    p.active = bool(active)

    db.session.add(p)
    db.session.commit()

    return True


def update_passbook(passbook_id, customer_name, address, id_number, phone, passbook_type_id, active=None):
    p = get_passbook_by_id(passbook_id=int(passbook_id))
    p.customer_name = customer_name
    p.address = address
    p.id_number = id_number
    p.phone = phone
    p.passbook_type_id = passbook_type_id
    if active:
        active = 'True'
    else:
        active = ''
    p.active = bool(active)

    db.session.add(p)
    db.session.commit()
    return True


def delete_passbook(passbook_id):
    p = get_passbook_by_id(passbook_id=passbook_id)
    db.session.delete(p)
    db.session.commit()
    return True


# receipt: deposit slip
def get_deposit_slip():
    return Receipt.query.filter(Receipt.receipt_type_id == 1).all()


def get_withdrawal_slip():
    return Receipt.query.filter(Receipt.receipt_type_id == 2).all()


def add_deposit_slip(passbook_id, customer_name, money, creator_id):
    d = Receipt()

    d.passbook_id = int(passbook_id)
    d.customer_name = customer_name
    d.created_date = datetime.datetime.now()
    d.money = float(money)
    d.receipt_type_id = 1
    d.creator_id = int(creator_id)

    p = get_passbook_by_id(passbook_id=passbook_id)
    p.money += float(money)

    db.session.add(d, p)
    db.session.commit()

    return True


def add_withdrawal_slip(passbook_id, customer_name, money, creator_id):
    d = Receipt()

    d.passbook_id = int(passbook_id)
    d.customer_name = customer_name
    d.created_date = datetime.datetime.now()
    d.money = float(money)
    d.receipt_type_id = 2
    d.creator_id = int(creator_id)

    p = get_passbook_by_id(passbook_id=passbook_id)
    p.money -= float(money)

    db.session.add(d, p)
    db.session.commit()

    return True


def get_user():
    return User.query.all()

