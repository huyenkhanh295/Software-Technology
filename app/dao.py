import datetime
from calendar import monthrange
from twilio.rest import Client
from app.models import *


# passbook
def get_passbook_by_id(passbook_id):
    return Passbook.query.get(passbook_id)


def get_passbook_type_by_id(passbooktype_id):
    return PassbookType.query.get(passbooktype_id)


def get_passbook(id=None, keyword=None):
    p = Passbook.query

    if keyword:
        p = p.filter(Passbook.customer_name.contains(keyword))
    if id:
        p = p.filter(Passbook.id == id)

    return p.all()


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


# receipt: withdrawal slip
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
    if not p.active:
        p.active = True

    db.session.add(d, p)
    db.session.commit()
    current_day = datetime.datetime.now().strftime('%H:%M %d/%m/%Y')
    message = "MeoBank: {} TK {}: +{:,.0f}VND. So du {:,.0f}VND.".format(current_day, p.id, float(money), p.money)
    phone = '+84' + p.phone[1:]
    send_sms(message_body=message, message_to=phone)
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

    if p.money == 0:
        p.active = False

    db.session.add(d, p)
    db.session.commit()
    current_day = datetime.datetime.now().strftime('%H:%M %d/%m/%Y')
    message = "MeoBank: {} TK {}: -{:,.0f}VND. So du {:,.0f}VND.".format(current_day, p.id, float(money), p.money)
    phone = '+84' + p.phone[1:]
    send_sms(message_body=message, message_to=phone)
    return True


def get_user():
    return User.query.all()


def get_expiration_date(passbook):
    expiration_date = None
    if passbook:
        passbook_type = get_passbook_type_by_id(passbooktype_id=passbook.passbook_type_id)
        term = int(passbook_type.type_name.split(" ")[0])

        month = passbook.created_date.month
        day = 0
        year = passbook.created_date.year
        if month + term <= 12:
            for i in range(month + 1, month + term + 1):
                day += monthrange(year, i)[1]

        expiration_date = passbook.created_date + datetime.timedelta(days=day)
    return expiration_date


def send_sms(message_body, message_to):
    account_sid = 'AC13dd6685365bc934fde39f97881a3fd3'
    auth_token = '42c23dcbe74889f30f8880b5afe0ecc6'
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        from_='+16029621577',
        body=message_body,
        to=message_to
    )

    print(message.sid)
