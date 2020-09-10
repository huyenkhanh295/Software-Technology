from flask import request, make_response, jsonify

from app.models import *

# Swagger
# def get_all_passbook():
#     get_passbook = Passbook.query.all()
#     passbook_schema = PassBookSchema(many=True)
#     passbooks = passbook_schema.dump(get_passbook)
#     return make_response(jsonify({"passbook": passbooks}))


def get_all_passbook():
    return Passbook.query.all()


def get_passbook_role():
    return PassbookRole.query.all()


def add_passbook(passbook):
    return passbook.create()


# Swagger
# def add_passbook():
#     data = request.get_json()
#     passbook_schema = PassBookSchema()
#     passbooks = passbook_schema.load(data)
#     result = passbook_schema.dump(passbooks.create())
#     return make_response(jsonify({"passbook": result}), 200)


def get_id_passbook(passbook_id):
    return Passbook.query.get(Passbook.id == passbook_id)
