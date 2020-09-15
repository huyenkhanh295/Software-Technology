from datetime import date

from flask import request, make_response, jsonify

from app.models import *


# Swagger
# def get_all_passbook():
#     get_passbook = Passbook.query.all()
#     passbook_schema = PassBookSchema(many=True)
#     passbooks = passbook_schema.dump(get_passbook)
#     return make_response(jsonify({"passbook": passbooks}))


def get_all_passbook_type():
    return PassbookType.query.all()


def get_passbook_type_by_id(passbooktype_id):
    return PassbookType.query.get(passbooktype_id)


def get_all_passbook():
    return Passbook.query.all()


def get_passbook_by_id(passbook_id):
    return Passbook.query.get(passbook_id)


def get_passbook_type():
    return PassbookType.query.all()


def add_rule(type_name, interest_rate):
    p = PassbookType()
    p.type_name = type_name
    p.interest_rate = interest_rate

    db.session.add(p)
    db.session.commit()

    return True


def update_rule(passbooktype_id, type_name, interest_rate):
    p = get_passbook_type_by_id(passbooktype_id=int(passbooktype_id))
    p.type_name = type_name
    p.interest_rate = interest_rate

    db.session.add(p)
    db.session.commit()
    return True


def delete_rule(passbooktype_id):
    p = get_passbook_type_by_id(passbooktype_id)
    db.session.delete(p)
    db.session.commit()
    return True


def add_passbook(customer_name, address, id_number, phone, money, passbook_type_id, active):
    p = Passbook()
    p.customer_name = customer_name
    p.address = address
    p.id_number = id_number
    p.phone = phone
    p.created_date = date.today()
    p.money = float(money)
    p.passbook_type_id = passbook_type_id
    if active == '':
        active = 'True'
    p.active = bool(active)

    db.session.add(p)
    db.session.commit()

    return True


def update_passbook(passbook_id, customer_name, address, id_number, phone, money, passbook_type_id, active='False'):
    p = get_passbook_by_id(passbook_id=int(passbook_id))
    p.customer_name = customer_name
    p.address = address
    p.id_number = id_number
    p.phone = phone
    p.money = float(money)
    p.passbook_type_id = passbook_type_id
    if active == '':
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

# Swagger
# def add_passbook():
#     data = request.get_json()
#     passbook_schema = PassBookSchema()
#     passbooks = passbook_schema.load(data)
#     result = passbook_schema.dump(passbooks.create())
#     return make_response(jsonify({"passbook": result}), 200)
