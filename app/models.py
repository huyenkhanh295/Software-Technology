import hashlib

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, event
from sqlalchemy.orm import relationship
from flask_admin.contrib.sqla import ModelView
from flask_admin import BaseView, expose
from flask_login import UserMixin, current_user, logout_user
from flask import redirect
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


admin.add_view(RoleView(Role, db.session))
admin.add_view(UserAdmin(User, db.session))
admin.add_view(AboutUsView(name="About Us"))
admin.add_view(LogoutView(name="Logout"))

if __name__ == "__main__":
    db.create_all()
