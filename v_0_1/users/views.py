from flask import request, Response
from flask.views import MethodView
from .models import *
from flask import jsonify, send_from_directory, g
import redis
import random
from .. import app
import os,time
from werkzeug.utils import secure_filename


# 阿里云接口包
import sys
from ..dysms_python.aliyunsdkdysmsapi.request.v20170525 import SendSmsRequest
from ..dysms_python.aliyunsdkdysmsapi.request.v20170525 import QuerySendDetailsRequest
from aliyunsdkcore.client import AcsClient
import uuid
from aliyunsdkcore.profile import region_provider
from aliyunsdkcore.http import method_type as MT
from aliyunsdkcore.http import format_type as FT
from ..dysms_python import const


class Index(MethodView):

    def __init__(self):
        pass

    @auth.login_required
    def get(self):
        return 'hello world!!!'


class ALiYun(MethodView):

    def __init__(self):
        self.phone = request.args.get('phone')
        try:
            reload(sys)
            sys.setdefaultencoding('utf8')
        except NameError:
            pass
        except Exception as err:
            raise err
        # 注意：不要更改
        REGION = "cn-hangzhou"
        PRODUCT_NAME = "Dysmsapi"
        DOMAIN = "dysmsapi.aliyuncs.com"
        self.acs_client = AcsClient(const.ACCESS_KEY_ID, const.ACCESS_KEY_SECRET, REGION)
        region_provider.add_endpoint(PRODUCT_NAME, REGION, DOMAIN)

    def send_sms(self, business_id, phone_numbers, sign_name, template_code, template_param=None):
        smsRequest = SendSmsRequest.SendSmsRequest()
        # 申请的短信模板编码,必填
        smsRequest.set_TemplateCode(template_code)
        # 短信模板变量参数
        if template_param is not None:
            smsRequest.set_TemplateParam(template_param)
        # 设置业务请求流水号，必填。
        smsRequest.set_OutId(business_id)
        # 短信签名
        smsRequest.set_SignName(sign_name)
        # 数据提交方式
        # smsRequest.set_method(MT.POST)
        # 数据提交格式
        # smsRequest.set_accept_format(FT.JSON)
        # 短信发送的号码列表，必填。
        smsRequest.set_PhoneNumbers(phone_numbers)
        # 调用短信发送接口，返回json
        smsResponse = self.acs_client.do_action_with_exception(smsRequest)
        # TODO 业务处理
        return smsResponse

    def get(self):
        __business_id = uuid.uuid1()
        # print(__business_id)
        verify_code = self.generate_verification_code()
        params = "{\"code\":"+"\""+verify_code+"\","+"\"product\":\"123\"}"
        # params = u'{"name":"wqb","code":"12345678","address":"bz","phone":"13000000000"}'
        print(self.send_sms(__business_id, self.phone, "苹果", "SMS_137785091", params))
        # print(send_sms(__business_id, "18579209598", "苹果", "SMS_137785091", params))
        # str_test = redis_node(self.phone, verify_code)
        """
        issue：此处应加入判断，当信息回馈为发送成功时才执行下面的将验证码存放到redis中的动作，暂放此处。
        """
        return redis_node(self.phone, verify_code)

    @staticmethod
    def generate_verification_code():
        """随机生成6位的验证码"""
        code_list = []
        for i in range(10):
            code_list.append(str(i))
        random_number = random.sample(code_list, 6)
        verification_code = ''.join(random_number)  # list to string
        return verification_code


class Register(MethodView):

    def __init__(self):
        self.phone = request.form.get('phone')
        self.code = request.form.get('code')
        self.pwd = request.form.get('pwd')

    def post(self):
        result = redis_node(self.phone, self.code)
        if result == "success":
            user = MembersInformation(password=self.pwd, phone=self.phone)
            db.session.add(user)
            db.session.commit()
            return jsonify({'code': '200', 'message': 'success'})
        else:
            return result


class Login(MethodView):

    def __init__(self):
        self.phone = request.form.get('phone')
        self.pwd = request.form.get('pwd')

    def post(self):
        result = MembersInformation.query.filter_by(phone=self.phone).first()
        if result is not None and result.verify_password(self.pwd):
            return jsonify({"code": "200", "message": "success", "balance": str(result.balance), "members_name":
                str(result.members_name), "pay_password": str(result.pay_password)})
        return jsonify({"code": "500", "message": "fail"})


# 获取token
class Token(MethodView):

    def __init__(self):
        pass

    @auth.login_required
    def get(self):
        token = g.user.generate_auth_token(600)
        return jsonify({'token': token.decode('ascii'), 'duration': 600})


class Logout(MethodView):

    def __init__(self):
        pass

    @auth.login_required
    def get(self):
        g.user.generate_auth_token(1)
        return jsonify({"code": "200", "message": "success"})


class ChangePassword(MethodView):

    def __init__(self):
        self.phone = request.form.get('phone')
        self.code = request.form.get('code')
        self.pwd = request.form.get('pwd')

    def post(self):
        result = redis_node(self.phone, self.code)
        if result == "success":
            str_result = MembersInformation.query.filter_by(phone=self.phone).first()
            str_result.password = self.pwd
            db.session.add(str_result)
            db.session.commit()
            return jsonify({"code": "200", "message": "success"})
        return result


class LoginChangePassword(MethodView):

    def __init__(self):
        self.phone = request.form.get('phone')
        self.old_pwd = request.form.get('old_pwd')
        self.new_pwd = request.form.get('new_pwd')

    def post(self):
        result = MembersInformation.query.filter_by(phone=self.phone).first()
        if result is not None and result.verify_password(self.old_pwd):
            result.password = self.new_pwd
            db.session.add(result)
            db.session.commit()
            return jsonify({"code": "200", "message": "success"})


# 将短信验证码存放在redis中并设置五分钟的过期时间
def redis_node(key_phone, value_code):
    """当有最新的发送验证码时会自动获取最新的验证码，待确认"""
    """操作频繁的情况下会导致该号码不能发送验证码，此异常暂未处理"""
    """redis操作"""
    print("1")
    node = redis.StrictRedis(host='127.0.0.1', port=6379)
    print("2")
    if request.method == 'POST':
        try:
            # 此处可能会导致获取不到该手机号码的验证码抛出异常
            """
            不加入.decode()会导致字符为（b'字符'）的格式
            """
            print("3")
            str_code = node.get(key_phone).decode()
        except AttributeError:
            print("4")
            return jsonify({"code": "500", "message": "fail", "detail": "没有该验证码"})
        print("5")
        if value_code == str_code:
            print(6)
            return "success"
        else:
            return jsonify({"code": "500", "message": "fail", "detail": "验证码错误"})
    if request.method == 'GET':
        node.set(key_phone, value_code)
        # 设置5分钟后过期
        node.expire(key_phone, 300)
        str_test = node.get(key_phone).decode()
        """
            在jsonify和json.dumps中如有数字非字符格式时会导致出错需用str()强转为字符串才正确
            TypeError: Object of type 'bytes' is not JSON serializable
            issue：此处，如发送信息的时候出现同一号码重复发送时会导致忙碌状态，信息发送不成功
        """
        return jsonify({"code": "200", "message": "success", "message_code": str(str_test)})


# 修改会员昵称：此处带有get方法可方便调试因curl不支持汉字会导致乱码
class ChangeMembersName(MethodView):

    def __init__(self):
        self.phone = request.form.get('phone')
        self.members_name = request.form.get('members_name')

        self.phone = request.args.get('phone')
        self.members_name = request.args.get('members_name')

    def post(self):
        print(self.members_name)
        result = MembersInformation.query.filter_by(phone=self.phone).first()
        result.members_name = self.members_name
        print(result.members_name)
        db.session.add(result)
        db.session.commit()
        return jsonify({"code": "200", "message": "success"})

    def get(self):
        print(self.members_name)
        result = MembersInformation.query.filter_by(phone=self.phone).first()
        result.members_name = self.members_name
        print(result.members_name)
        db.session.add(result)
        db.session.commit()
        return jsonify({"code": "200", "message": "success"})


# 获取图片
class GetImage(MethodView):

    def __init__(self):
        self.phone = request.args.get('phone')

    def get(self):
        result = MembersInformation.query.filter_by(phone=self.phone).first()
        return send_from_directory('./users/img', result.image_name+'.jpg')


# 上传图片
class UploadImage(MethodView):

    def __init__(self):
        self.phone = request.form.get('phone')
        # self.new_filename = request.form.get('filename')

        # self.form_name = 'myfile' # 测试
        self.form_name = request.form.get('formname')
        self.basedir = os.path.abspath(os.path.dirname(__file__))
        self.ALLOWED_EXTENSIONS = set(['txt', 'png', 'jpg', 'xls', 'JPG', 'PNG', 'xlsx', 'gif', 'GIF'])

    # 用于判断文件后缀
    def allowed_file(self, filename):
        return '.' in filename and filename.rsplit('.', 1)[1] in self.ALLOWED_EXTENSIONS

    def post(self):
        upload_folder = "img" # 定义上传的文件夹路径
        file_dir = os.path.join(self.basedir, upload_folder)
        if not os.path.exists(file_dir):
            os.makedirs(file_dir)
        f = request.files[self.form_name]  # 从表单的file字段获取文件，myfile为该表单的name值
        if f and self.allowed_file(f.filename):  # 判断是否是允许上传的文件类型
            file_name = secure_filename(f.filename)
            ext = file_name.rsplit('.', 1)[1]  # 获取文件后缀
            unix_time = int(time.time()) # 返回当前时间的时间戳（1970纪元后经过的浮点秒数）。
            new_filename = str(unix_time) + '.' + ext  # 修改了上传的文件名
            f.save(os.path.join(file_dir, new_filename))  # 保存文件到img目录

            # self.save_imagename(new_filename) # 文件上传成功后再保存到目录中,此处改成get方法测试过，post无法模拟
            # 同时传递文件和参数

            return jsonify({"code": "200", "message": "success"})
        else:
            return jsonify({"code": "500", "message": "fail"})

    # 保存用户的图片名称到数据库中
    def save_imagename(self, new_filename):
        result = MembersInformation.query.filter_by(phone=self.phone).first()
        # 此处若没有相片图片则为新增，若有则为修改
        result.image_name = new_filename
        db.session.add(result)
        db.session.commit()
        return jsonify({"code": "200", "message": "success"})


# 充值提现记录
class TransactionAndDetail(MethodView):

    def __init__(self):
        self.phone = request.args.get('phone')

    def get(self):
        # 此处用于get方法添加测试数据
        # transactiondetail = TransactionDetail(phone=self.phone)
        # db.session.add(transactiondetail)
        # db.session.commit()
        # return jsonify({'code': '200', 'message': 'success'})
        result = TransactionDetail.query.filter(phone=self.phone).all()
        reduce_list, add_list, transaction_list = []
        for str_result in result:
            reduce_list.append(str_result.reduce_price)
            add_list.append(str_result.add_price)
            transaction_list.append(str_result.transaction_time)
        return jsonify({"code": "200", "message": "success", "reduce_price": reduce_list, "add_price": add_list,
                        "transaction_time": transaction_list})


# 添加实名认证
class VerifyTrueName(MethodView):

    def __init__(self):
        self.phone = request.form.get('phone')
        self.id_card = request.form.get('idcard')
        self.true_name = request.form.get('truename')

    def post(self):
        result = MembersInformation.query.filter_by(phone=self.phone).first()
        result.id_card = self.id_card
        result.true_name = self.true_name
        db.session.add(result)
        db.session.commit()
        return jsonify({"code": "200", "message": "success"})


# 充值
class AddPrice(MethodView):

    def __init__(self):
        self.phone = request.form.get('phone')
        self.price = request.form.get('price')

    # 在添加充值金额的时候添加一笔数据到充值提现记录表中
    def post(self):
        result = MembersInformation.query.filter_by(phone=self.phone).first()
        transaction_result = TransactionDetail.query.filter_by(phone=self.phone).first()
        transaction_result.phone = self.phone
        transaction_result.add_price = self.price
        result.balance = str(float(result.balance) + float(self.price))
        print(result.balance)
        db.session.add(result)
        db.session.add(transaction_result)
        db.session.commit()
        return jsonify({"code": "200", "message": "success"})


# 提现
class ReducePrice(MethodView):

    def __init__(self):
        self.phone = request.form.get('phone')
        self.price = request.form.get('price')

    # 在提现金额的时候添加一笔数据到充值提现记录表中
    def post(self):
        result = MembersInformation.query.filter_by(phone=self.phone).first()
        transaction_result = TransactionDetail.query.filter_by(phone=self.phone).first()
        transaction_result.phone = self.phone
        transaction_result.reduce_price = self.price
        result.balance = str(float(result.balance) - float(self.price))
        print(result.balance)
        db.session.add(result)
        db.session.add(transaction_result)
        db.session.commit()
        return jsonify({"code": "200", "message": "success"})


# 设置支付密码
class AddOrUpdatePayPassword(MethodView):

    def __init__(self):
        self.phone = request.form.get('phone')
        self.pay_password = request.form.get('paypassword')

    def post(self):
        result = MembersInformation.query.filter_by(phone=self.phone).first()
        result.pay_password = self.pay_password
        db.session.add(result)
        db.session.commit()
        return jsonify({"code": "200", "message": "success"})