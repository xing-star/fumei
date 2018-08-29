from .. import db
from .. import app
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)
from flask_httpauth import HTTPBasicAuth
from flask import g

auth = HTTPBasicAuth()


# 会员信息：唯一标识，手机号码，密码，余额(可用余额)，会员姓名，头像文件名，身份证号，真实姓名，注册时间
class MembersInformation(db.Model):
    __tablename__ = 'members_information'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    phone = db.Column(db.String(20))
    # 此处若命名为password会导致冲突发生，使得flask_migrate无法映射生成表结构
    password_hash = db.Column(db.String(128))
    balance = db.Column(db.String(20))
    members_name = db.Column(db.String(20))
    image_name = db.Column(db.String(30))
    id_card = db.Column(db.String(30))
    true_name = db.Column(db.String(60))
    pay_password = db.Column(db.String(20))
    register_time = db.Column(db.DateTime(), default=datetime.now())

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_auth_token(self, expiration):
        s = Serializer(app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'id': self.id})

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None  # valid token, but expired
        except BadSignature:
            return None  # invalid token
        user = MembersInformation.query.get(data['id'])
        return user


@auth.verify_password
def verify_password(username_or_token, password):
    # first try to authenticate by token
    user = MembersInformation.verify_auth_token(username_or_token)
    if not user:
        # try to authenticate with username/password
        user = MembersInformation.query.filter_by(phone=username_or_token).first()
        print("user+++")
        if not user or not user.verify_password(password):
            return False
    g.user = user
    print("user")
    return True


# 充值提现交易明细：唯一标识，手机号码，提现，充值，交易时间
class TransactionDetail(db.Model):
    __tablename__ = 'transaction_detail'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    phone = db.Column(db.String(20))
    reduce_price = db.Column(db.String(20))
    add_price = db.Column(db.String(20))
    transaction_time = db.Column(db.DateTime(), default=datetime.now())
