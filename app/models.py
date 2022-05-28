from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

from flask_wtf import FlaskForm
from werkzeug.security import  check_password_hash
import pymysql, os
from wtforms import StringField, SubmitField

app = Flask(__name__)

# 数据库配置
HOSTNAME = 'localhost'
PORT = '3306'
DATABASE = 'movic'
USERNAME = 'root'
PASSWORD = 'Wsw981017@'

app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format(USERNAME, PASSWORD, HOSTNAME, PORT, DATABASE)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config["SECRET_KEY"] = os.urandom(24)
db = SQLAlchemy(app)


# 会员
class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), unique=True)
    pwd = db.Column(db.String(100))
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)
    userlogs = db.relationship("UserLog", backref="user")  # 会员日志外键关联
    def __repr__(self):
        return "<User %r>" % self.name

    def check_pwd(self, pwd):
        return check_password_hash(self.pwd, pwd)

class LexicalRules(db.Model):
    __tablename__="LexicalRules"
    id = db.Column(db.Integer,primary_key=True, autoincrement=True)
    ComplexWord = db.Column(db.TEXT)
    SimpleWord = db.Column(db.TEXT)

class largelexicalRules(db.Model):
    __tablename__="largelexicalRules"
    id = db.Column(db.Integer,primary_key=True, autoincrement=True)
    complexWord = db.Column(db.TEXT)
    simpleWord = db.Column(db.TEXT)

class SyntacticRules(db.Model):
    __tablename__="SyntacticRules"
    id = db.Column(db.Integer,primary_key=True, autoincrement=True)
    ComplexStructure = db.Column(db.TEXT)
    SimpleStructure = db.Column(db.TEXT)

class SyntacticRulesLargewithScore(db.Model):
    __tablename__="SyntacticRulesLargewithScore"
    id = db.Column(db.Integer,primary_key=True, autoincrement=True)
    ComplexStructure = db.Column(db.TEXT)
    SimpleStructure = db.Column(db.TEXT)
    score = db.Column(db.FLOAT)

class largelexicalruleswithScore(db.Model):
    __tablename__="largelexicalruleswithScore"
    id = db.Column(db.Integer,primary_key=True, autoincrement=True)
    ComplexWord = db.Column(db.TEXT)
    SimpleWord = db.Column(db.TEXT)
    score = db.Column(db.FLOAT)

class CollectData(db.Model):
    __tablename__="Collect_data"
    id = db.Column(db.Integer,primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer)
    item_id = db.Column(db.Integer)
    collect_lexical =db.Column(db.TEXT)
    collect_syntactic = db.Column(db.TEXT)
    input_lexical = db.Column(db.TEXT)
    input_syntactic = db.Column(db.TEXT)



class UserLog(db.Model):
    """
    会员登录日志表
    """
    __tablename__ = "userlog"  # 表名
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 编号
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # 所属会员
    ip = db.Column(db.String(100))  # 登录IP
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)  # 登录时间；

    def __repr__(self):
        return "<UserLog %r>" % self.id

class Userlabeled(db.Model):
    """
    每个用户标记了啥
    """
    __tablename__ = "Userlabeled"
    userid = db.Column(db.Integer,primary_key=True)
    labeled = db.Column(db.TEXT)

class Sentence(db.Model):
    """
    每个句子被标了几次
    """
    __tablename__ = "Sentence"
    id = db.Column(db.Integer,primary_key=True)
    frequency = db.Column(db.Integer)

if __name__ == '__main__':
    db.drop_all()
    db.create_all()
