from .. import app
from .views import *
"""
Issue:经测试，首次新号码发送验证码，在注册和修改密码时都会“卡”一段时间
经排查，在为到达post方法之前属于卡顿时间，说明不是代码的问题，具体问题待
处理。
Issue:经测试，添加数据的时候同一请求添加的datetime.now()的时间都是一致不会变化的。
"""


def usersrouter():
    app.add_url_rule('/', view_func=Index.as_view('/'), methods=['GET'])
    # 获取阿里云短信验证码接口
    app.add_url_rule('/fumei/users/getaliyuncode', view_func=ALiYun.as_view('/fumei/users/getaliyuncode'),
                     methods=['GET'])
    # 用户注册路由
    app.add_url_rule('/fumei/users/register', view_func=Register.as_view('/fumei/users/register'),
                     methods=['POST'])
    # 用户登录路由
    app.add_url_rule('/fumei/users/login', view_func=Login.as_view('/fumei/users/login'),
                     methods=['POST'])
    # 获取token
    app.add_url_rule('/fumei/users/token', view_func=Token.as_view('/fumei/users/token'),
                     methods=['GET'])
    # 注销登录（此处采用直接设置token过期来注销登录）Issue：此处设置过期时间无效
    app.add_url_rule('/fumei/users/logout', view_func=Logout.as_view('/fumei/users/logout'),
                     methods=['GET'])
    # 用户未登录修改密码的路由（忘记密码）
    app.add_url_rule('/fumei/users/changepassword', view_func=ChangePassword.as_view('/fumei/users/changepassword'),
                     methods=['POST'])
    # 用户登录修改密码
    app.add_url_rule('/fumei/users/loginchangepassword', view_func=LoginChangePassword
                     .as_view('/fumei/users/loginchangepassword'), methods=['POST'])
    # 修改昵称
    app.add_url_rule('/fumei/users/changemembersname',
                     view_func=ChangeMembersName.as_view('/fumei/users/changemembersname'), methods=['POST', 'GET'])
    # 获取头像图片
    app.add_url_rule('/fumei/users/getimage', view_func=GetImage.as_view('/fumei/users/getimage'),
                     methods=['POST', 'GET'])
    # 上传图片
    app.add_url_rule('/fumei/users/uploadimage', view_func=UploadImage.as_view('/fumei/users/uploadimage'),
                     methods=['POST', 'GET'])
    # 充值提现交易记录
    app.add_url_rule('/fumei/users/transactionanddetail', view_func=TransactionAndDetail
                     .as_view('/fumei/users/transactionanddetail'), methods=['GET'])
    # 添加实名认证
    app.add_url_rule('/fumei/users/verifytruename', view_func=VerifyTrueName.as_view('/fumei/users/verifytruename'),
                     methods=['POST'])
    # 充值
    app.add_url_rule('/fumei/users/addprice', view_func=AddPrice.as_view('/fumei/users/addprice'), methods=['POST'])
    # 提现
    app.add_url_rule('/fumei/users/reduceprice', view_func=ReducePrice.as_view('/fumei/users/reduceprice'),
                     methods=['POST'])
    # 设置支付密码
    app.add_url_rule('/fumei/users/addorupdatepaypassword', view_func=AddOrUpdatePayPassword
                     .as_view('/fumei/users/addorupdatepaypassword'), methods=['POST'])

