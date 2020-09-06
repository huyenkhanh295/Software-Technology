import hashlib
from dataclasses import dataclass

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, event, DateTime, Float
from sqlalchemy.orm import relationship
from flask_admin.contrib.sqla import ModelView
from flask_admin import BaseView, expose
from flask_login import UserMixin, current_user, logout_user
from flask import redirect
from marshmallow_sqlalchemy import ModelSchema
from marshmallow import fields
from app import db, admin


class Role(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    users = relationship('User', backref='role', lazy=True)

    # lay chuoi dai dien: hien thi tren bang user thay cho cot role id
    def __str__(self):
        return self.name


class User(db.Model, UserMixin):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    active = Column(Boolean, default=True)
    username = Column(String(50), nullable=False)
    password = Column(String(50), nullable=False)
    role_id = Column(Integer, ForeignKey(Role.id), nullable=False)

    def __str__(self):
        return self.name


class PassbookRole(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    interest_rate = Column(Float, nullable=False)
    passbooks = relationship('Passbook', backref='PassbookRole', lazy=True)

    # lay chuoi dai dien: hien thi tren bang user thay cho cot role id

    def __str__(self):
        return self.name


# @dataclass
class Passbook(db.Model, UserMixin):
    __tablename__ = "passbook"
    id = Column(Integer, primary_key=True, autoincrement=True)
    customer_name = Column(String(50), nullable=False)
    address = Column(String(50), nullable=False)
    date_create = Column(DateTime(50), nullable=False)
    money = Column(Float, nullable=False)
    phone_number = Column(Integer, nullable=False)
    id_number = Column(String(20), nullable=False)
    passbook_role_id = Column(Integer, ForeignKey(PassbookRole.id), nullable=False)

    def __str__(self):
        return self.customer_name

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    # def __init__(self, customer_name, address, date_create, money, phone_number, id_number, passbook_role_id):
    #     self.customer_name = customer_name
    #     self.address = address
    #     self.date_create = date_create
    #     self.money = money
    #     self.phone_number = phone_number
    #     self.id_number = id_number
    #     self.passbook_role_id = passbook_role_id

    def __repr__(self):
        return '' % self.id

    db.create_all()


class PassBookSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = Passbook
        sqla_session = db.session

    id = fields.Number(dump_only=True)
    customer_name = fields.String(required=True)
    address = fields.String(required=True)
    date_create = fields.DateTime(required=True)
    money = fields.Float(required=True)
    phone_number = fields.Integer(required=True)
    id_number = fields.Integer(required=True)
    passbook_role_id = fields.Integer(required=True)


class AboutUsView(BaseView):
    @expose("/")
    def index(self):
        return self.render("admin/about-us.html")


class LogoutView(BaseView):
    @expose()
    def index(self):
        logout_user()

        return redirect("/admin")

    def is_accessible(self):
        return current_user.is_authenticated


@event.listens_for(User.password, 'set', retval=True)
def hash_user_password(target, value, oldvalue, initiator):
    if value != oldvalue:
        value = str(hashlib.md5(value.strip().encode("utf-8")).hexdigest())
        return value
    return value


# Customized admin interface
class CustomView(ModelView):
    list_template = '/admin/list.html'
    create_template = '/admin/create.html'
    edit_template = '/admin/edit.html'
    column_display_pk = True
    form_excluded_columns = ['users', ]

    def is_accessible(self):
        return current_user.is_authenticated


class UserAdmin(CustomView):
    column_searchable_list = ('name',)
    column_filters = ('name', 'role_id')
    page_size = 10


class RoleView(CustomView):
    can_create = False
    can_edit = False
    can_delete = False


class PassbookView(ModelView):
    can_create = True
    can_edit = True
    can_delete = True
    page_size = 10


class PassbookRoleView(ModelView):
    can_create = True
    can_edit = True
    can_delete = True
    page_size = 10


admin.add_view(RoleView(Role, db.session))
admin.add_view(UserAdmin(User, db.session))
admin.add_view(AboutUsView(name="About Us"))
admin.add_view(LogoutView(name="Logout"))
admin.add_view(PassbookView(Passbook, db.session))
admin.add_view(PassbookRoleView(PassbookRole, db.session))

if __name__ == "__main__":
    db.create_all()
