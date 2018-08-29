from .. import app
from .views import *


def marketrouter():
    # 搜索框根据代码与发行人进行搜索
    app.add_url_rule('/market/searchusers', view_func=SearchUsers.as_view('/market/searchusers'), methods=['GET'])

    # 添加上市人信息，后期用于web后台管理界面
    app.add_url_rule('/market/addusersinformation', view_func=AddUsersInformation.
                     as_view('/market/addusersinformation'), methods=['GET'])
