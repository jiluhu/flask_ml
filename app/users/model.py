#-*- coding: UTF-8 -*-
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.security import generate_password_hash, check_password_hash

from app import db

class Users(db.Model):
    # 表的名字:
    __tablename__ = 'link_user'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(250),  unique=True, nullable=False)
    user_name = db.Column(db.String(250),  unique=True, nullable=False)
    password = db.Column(db.String(250))



    def __init__(self, user_name, password, email):
        self.user_name = user_name
        self.password = self.set_password(password)
        self.email = email

    def __str__(self):
        return "Users(id='%s')" % self.id

    def set_password(self, password):
        return generate_password_hash(password)

    def check_password(self, hash, password):
        return check_password_hash(hash, password)

    def get(id):
        return Users.query.filter_by(id=id).first()

    @staticmethod
    def add(user):
        db.session.add(user)
        return session_commit()

    def update(self):
        return session_commit()

    def delete(self, id):
        self.query.filter_by(id=id).delete()
        return session_commit()


def session_commit():
    try:
        db.session.commit()
    except SQLAlchemyError as e:
        db.session.rollback()
        reason = str(e)
        return reason
