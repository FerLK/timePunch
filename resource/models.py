#set up dn inside __init__.py
from db import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime, timedelta


class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, index=True)
    email = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    working = db.Column(db.Boolean, default=False)

    work = db.relationship('Work', backref="nameRef", lazy='dynamic')

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.working = False
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"User -> {self.name} ; id -> {self.id}; email -> {self.email}; working -> {self.working};  "

    def report_work(self):
        for wor in self.work:
            print(wor.work_name)

    def all_work(self):
        all_w = []
        all_w = self.work
        return all_w


class Work(db.Model):
    __tablename__ = "works"
    id = db.Column(db.Integer, primary_key=True)
    work_name = db.Column(db.String(64), index=True)
    work_local = db.Column(db.String(64), index=True)
    time_init = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    time_final = db.Column(db.DateTime)
    active = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, name, local, user_id, time_init):
        self.work_name = name
        self.work_local = local
        self.time_init = time_init
        self.time_final = time_init + timedelta(hours=8)
        self.active = True
        self.user_id = user_id
        # self.work_name = datetime.now().strftime("%x")

    def finalize(self):
        self.time_final = datetime.datetime.now()
        self.active = False

    def __repr__(self):
        return f"{self.time_init.strftime('%x')} Begin: {self.time_init.strftime('%X')} End: {self.time_final.strftime('%X')}"