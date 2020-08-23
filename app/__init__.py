from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_login import LoginManager

app = Flask(__name__)
app.secret_key = "\x189\xb1\r\x10\xe9\xb4\xb4H\xa0x-\x01R\xf0\xf7"
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:123456@localhost/qlsotietkiemdb?charset=utf8mb4"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

db = SQLAlchemy(app=app)

admin = Admin(app=app, name="QUẢN LÍ NGƯỜI DÙNG HỆ THỐNG", base_template='/admin/layout-admin.html', template_mode="bootstrap3")

login = LoginManager(app)


