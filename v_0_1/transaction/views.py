from flask import request, jsonify
from flask.views import MethodView
from .models import *
import datetime
from sqlalchemy import and_


class BuyTime(MethodView):

    def __init__(self):
        self.paycode = request.args.get('pay_code')
        self.payprice = request.args.get('pay_price')
        self.paycount = request.args.get('pay_count')
        self.phone = request.args.get('phone')

    def post(self):
        now_time = datetime.datetime.now().strftime('%Y-%m-%d')
        result = PayOrders.query.filter(status=0, order_time=now_time).order_by(PayOrders.order_time.desc()).all
        for str_result in result:
            print(str_result.id)
            print(str_result.phone)
            print(str_result.pay_code)
            print(str_result.pay_price)
            print(str_result.pay_count)
            print("-------------------")
        # 添加记录到订单表中，status状态栏成交为1，未成交为0，成交后插入持有资产表中
        orders = PayOrders(pay_code=self.paycode, pay_price=self.payprice, pay_count=self.paycount)
        db.session.add(orders)
        db.session.commit()

    def get(self):
        now_time = datetime.datetime.now().strftime('%Y-%m-%d')
        # db.cast(PayOrders.order_time, db.Date) == (db.cast(now_time, db.Date)) （当天时间）
        # 查询当天未成交的订单，status == 0（未成交状态）
        # 类型，购买匹配出售（‘sell’)
        # pay_code购买哪个上市人的时间
        # pay_price出价要高于或者等于售价才会匹配
        # Issue此中排列顺序是按时间先后顺序排列，如同一时间的情况下出价较高的人优先匹配没有实现
        result = PayOrders.query.filter(and_(db.cast(PayOrders.order_time, db.Date) == (db.cast(now_time, db.Date)),
                                             PayOrders.status == 0,
                                             PayOrders.pay_type == 'sell',
                                             PayOrders.pay_code == self.paycode,
                                             PayOrders.pay_price <= float(self.payprice))).all()
        # 当暂时无订单与其匹配时直接将该笔购买记录写入订单表status=0，未交易状态。
        if result is None:
            orders = PayOrders(phone=self.phone, pay_type='buy', pay_code=self.pay_code,
                               pay_price=self.pay_price,
                               pay_count=self.pay_count, status=0)
            db.session.add(orders)
            db.session.commit()
            return jsonify({"code": "200", "message": "add orders success"})
        id_list, phone_list, paycode_list, payprice_list, paycount_list = [], [], [], [], []
        for str_result in result:
            id_list.append(str_result.id)
            phone_list.append(str_result.phone)
            paycode_list.append(str_result.pay_code)
            payprice_list.append(str_result.pay_price)
            paycount_list.append(str_result.pay_count)
        # 购买数量依次匹配相应的订单数量

        # 2.如订单数量大于购买数量
        # 3.如订单数量小于购买数量

        """
        1.如符合条件的第一笔订单数量等于购买数量,则该笔交易已完成，将该笔订单的sell订单修改其状态为已完成
        并将该笔购买记录写入订单表中且状态也是已完成状态。
        """
        if paycount_list[0] == self.paycount:
            just_result = PayOrders.query.filter_by(id=id_list[0]).first()
            just_result.status = '1'
            orders = PayOrders(phone=self.phone, pay_type='buy', pay_code=self.pay_code,
                                                               pay_price=self.pay_price,
                                                               pay_count=self.pay_count, status=1)
            db.session.add(orders)
            db.session.add(just_result)
            db.session.commit()
            return jsonify({"code": "200", "message": "success"})
        """
        2.如符合条件的第一笔订单数量大于购买数量，则将该笔订单success_paycount设置为该笔购买数量，且该订单的总数量
        pay_count相应减少其购买的数量。状态依然为0，交易未完成状态。这笔购买记录为已完成状态。
        """
        if paycount_list[0] > self.paycount:
            just_result = PayOrders.query.filter_by(id=id_list[0]).first()
            just_result.success_paycount = self.paycount
            just_result.pay_count = paycount_list[0] - self.paycount
            orders = PayOrders(phone=self.phone, pay_type='buy', pay_code=self.pay_code,
                               pay_price=self.pay_price,
                               pay_count=self.pay_count, status=1)
            db.session.add(just_result)
            db.session.add(orders)
            db.session.commit()
        for str_count in paycount_list:
            if str_count == self.paycount:
                pass
        return jsonify({"code": "200", "message": "success", "id_list": id_list,
                        "phone_list": phone_list, "paycode_list": paycode_list,
                        "payprice_list": payprice_list, "paycount_list": paycount_list})


class TestAddOrders(MethodView):

    def __init__(self):
        self.phone = request.args.get('phone')
        self.pay_type = request.args.get('pay_type')
        self.pay_code = request.args.get('pay_code')
        self.pay_price = request.args.get('pay_price')
        self.pay_count = request.args.get('pay_count')
        self.status = request.args.get('status')

    def get(self):
        orders = PayOrders(phone=self.phone, pay_type=self.pay_type, pay_code=self.pay_code, pay_price=self.pay_price,
                           pay_count=self.pay_count, status=self.status)
        db.session.add(orders)
        db.session.commit()
        return jsonify({"code": "200", "message": "success"})


# 出售资产（时间）
class SellTime(MethodView):

    def __init__(self):
        pass

    def post(self):
        pass


# class PayOrders(db.Model):
#     __tablename__ = 'pay_orders'
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     phone = db.Column(db.String(20))
#     pay_code = db.Column(db.String(10))
#     pay_price = db.Column(db.String(20))
#     pay_count = db.Column(db.String(20))
#     success_paycount = db.Column(db.String(20))
#     status = db.Column(db.String(20))
#     order_time = db.Column(db.DateTime(), default=datetime.now())
# 查询订单
class QueryOrder(MethodView):

    def __init__(self):
        self.phone = request.args.get('phone')

    def post(self):
        result = PayOrders.query.filter_by(phone=self.phone).all()
        pay_codelist, pay_pricelist, pay_countlist, success_paycountlist, statuslist, order_timelist = []
        for str_result in result:
            pay_codelist.append(str_result.pay_code)
            pay_pricelist.append(str_result.pay_price)
            pay_countlist.append(str_result.pay_count)
            success_paycountlist.append(str_result.success_paycount)
            statuslist.append(str_result.status)
            order_timelist.append(str_result.order_time)
        return jsonify({"code": "200", "message": "success", "pay_code": pay_codelist,
                        "pay_price": pay_pricelist, "pay_count": pay_countlist,
                        "success_paycount": success_paycountlist, "status": statuslist, "order_time": order_timelist})


# 取消订单逻辑
# 1.status变成00
# 2.将订单的钱转到原来的账户上
class CancelOrder(MethodView):

    def __init__(self):
        pass

    def post(self):
        pass


# 持有资产时间
class HoldTime(MethodView):

    def __init__(self):
        pass

    def post(self):
        pass


# 已成交明细
class DealDetail(MethodView):

    def __init__(self):
        self.phone = request.args.get('phone')

    def post(self):
        result = PayDetail.query.filter(phone=self.phone).all()
        code_list, money_list, count_list, profitloss_list, time_list = []
        for str_result in result:
            code_list.append(str_result.history_paycode)
            money_list.append(str_result.history_paymoney)
            count_list.append(str_result.history_paycount)
            profitloss_list.append(str_result.history_profitloss)
            time_list.append(str_result.history_paytime)
        return jsonify({"code": "200", "message": "success", "history_paycode": code_list,
                        "history_paymoney": money_list, "history_paycount": count_list,
                        "history_profitloss": profitloss_list, "history_paytime": time_list})
