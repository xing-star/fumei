from .. import db
from datetime import datetime


# 持仓信息：唯一标识，持有人电话号码，持有发行代码，市值，持有数量，持有可交易数量，当前价格，成本，盈亏，持有时间
class HoldInformation(db.Model):
    __tablename__ = 'hold_information'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    phone = db.Column(db.String(20))
    pay_code = db.Column(db.String(10))
    pay_count = db.Column(db.String(20))
    hold_count = db.Column(db.String(20))
    can_pay = db.Column(db.String(20))
    present_price = db.Column(db.String(20))
    cost_price = db.Column(db.String(20))
    loss_price = db.Column(db.String(20))
    hold_time = db.Column(db.DateTime(), default=datetime.now())


# 交易明细：唯一标识，持有人电话号码，已交易发行代码，已交易的价格，已交易额，盈亏额，历史交易时间
class PayDetail(db.Model):
    __tablename__ = 'pay_detail'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    phone = db.Column(db.String(20))
    history_paycode = db.Column(db.String(10))
    history_paymoney = db.Column(db.String(20))
    history_paycount = db.Column(db.String(20))
    history_profitloss = db.Column(db.String(20))
    history_paytime = db.Column(db.DateTime(), default=datetime.now())


# 订单：唯一标识，持有人手机号码，交易类型（sell,buy）,发行代码，委托价格，委托数量，成交量，状态，订单时间
class PayOrders(db.Model):
    __tablename__ = 'pay_orders'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    phone = db.Column(db.String(20))
    pay_type = db.Column(db.String(20))
    pay_code = db.Column(db.String(10))
    pay_price = db.Column(db.String(20))
    pay_count = db.Column(db.String(20))
    success_paycount = db.Column(db.String(20))
    status = db.Column(db.String(20))
    order_time = db.Column(db.DateTime(), default=datetime.now())
