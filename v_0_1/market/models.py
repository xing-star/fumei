from .. import db
from datetime import datetime


# 基础交易详细页面：唯一标识，发行代码，最高价，最低价，开盘价
class BaseUsersByDay(db.Model):
    __tablename__ = 'base_usersbyday'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    pay_code = db.Column(db.String(10))
    hight_price = db.Column(db.String(10))
    low_price = db.Column(db.String(10))
    today_startprice = db.Column(db.String(10))


# 自定义:唯一标识，手机号码，发行代码
class OwnBaseUser(db.Model):
    __tablename__ = 'own_baseuser'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    phone = db.Column(db.String(20))
    pay_code = db.Column(db.String(10))


# 上市人信息:唯一标识，发行代码，发行人姓名，交易时间（流通时间），总价（该上市人的总身价），上市时间
class UsersInformation(db.Model):
    __tablename__ = 'users_information'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    pay_code = db.Column(db.String(10))
    pay_name = db.Column(db.String(20))
    transaction_time = db.Column(db.String(10))
    total_price = db.Column(db.String(20))
    image_name = db.Column(db.String(30))
    pay_time = db.Column(db.DateTime(), default=datetime.now())


# 日k线图数据,时间间隔为一天一次：唯一标识，发行代码，当前价格，涨跌百分数，当天时间
class UsersPayByDay(db.Model):
    __tablename__ = 'users_paybyday'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    pay_code = db.Column(db.String(10))
    now_price = db.Column(db.String(10))
    ups_downsprice = db.Column(db.String(10))
    pay_time = db.Column(db.DateTime(), default=datetime.now())


# 分时k线图数据,时间间隔为一分钟一次数据：唯一标识，发行代码，当前价格，涨跌百分数，交易时间
# 注：即时刷新的数据可不做持久化的动作存放在缓存redis中进行计算
class UsersPayByMinute(db.Model):
    __tablename__ = 'users_paybyminute'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    pay_code = db.Column(db.String(10))
    now_price = db.Column(db.String(10))
    ups_downsprice = db.Column(db.String(10))
    pay_time = db.Column(db.DateTime(), default=datetime.now())