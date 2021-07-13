from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
# pylint: disable=no-member

# 定义table
class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000)) # 存路径 
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    liked=db.Column(db.Integer,default=0) # liked 数量
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    notes = db.relationship('Note')
