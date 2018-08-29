from .. import app
from .views import *


def transactionrouter():
    # 购买时间
    app.add_url_rule('/fumei/transaction/buytime', view_func=BuyTime
                     .as_view('/fumei/transaction/buytime'), methods=['POST', 'GET'])
    # 出售时间
    app.add_url_rule('/fumei/transaction/selltime', view_func=SellTime
                     .as_view('/fumei/transaction/selltime'), methods=['POST'])
    # 查询订单
    app.add_url_rule('/fumei/transaction/queryorder', view_func=QueryOrder
                     .as_view('/fumei/transaction/queryorder'), methods=['GET'])
    # 取消订单
    app.add_url_rule('/fumei/transaction/cancelorder', view_func=CancelOrder
                     .as_view('/fumei/transaction/cancelorder'), methods=['POST'])
    # 添加订单测试信息
    app.add_url_rule('/fumei/transaction/testaddorders', view_func=TestAddOrders
                     .as_view('/fumei/transaction/testaddorders'), methods=['GET'])
    # 持仓查询
    app.add_url_rule('/fumei/transaction/holdtime', view_func=HoldTime
                     .as_view('/fumei/transaction/holdtime'), methods=['GET'])
    # 成交明细查询
    app.add_url_rule('/fumei/transaction/dealdetail', view_func=DealDetail.as_view('/fumei/transaction/dealdetail'),
                     methods=['GET'])
