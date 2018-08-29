from flask.views import MethodView
from flask import jsonify, request
from .models import *
from sqlalchemy import or_


class AddUsersInformation(MethodView):

    def __init__(self):
        self.pay_code = request.args.get('pay_code')
        self.pay_name = request.args.get('pay_name')
        self.transaction_time = request.args.get('transaction_time')
        self.total_price = request.args.get('total_price')
        self.image_name = request.args.get('image_name')

    def get(self):
        user = UsersInformation(pay_code=self.pay_code, pay_name=self.pay_name, transaction_time=self.transaction_time,
                                total_price=self.total_price, image_name=self.image_name)
        db.session.add(user)
        db.session.commit()
        return "register success"


class SearchUsers(MethodView):

    def __init__(self):
        self.code_or_name = request.args.get('code_or_name')

    def get(self):
        # 此处可以分为根据姓名或者发行代码来进行查询
        user_information = UsersInformation.query.filter(
            or_(UsersInformation.pay_code.like("%" + self.code_or_name + "%"),
                UsersInformation.pay_name.like("%" + self.code_or_name + "%"))
            ).all()
        paycode_list = []
        payname_list = []
        for str_user in user_information:
            paycode_list.append(str_user.pay_code)
            payname_list.append(str_user.pay_name)
        return jsonify({"code": paycode_list, "name": payname_list})