#### 文件夹目录介绍

- market（行情市场）

- transaction（交易）

- users（用户会员）

#### 使用Python虚拟环境

- 安装virtualenv
`pip install virtualenv`

- 创建虚拟环境
`virtualenv myvenv`
-(会在当前目录下生成myvenv的文件夹)
************
- 激活虚拟环境
  1.`cd myvenv\Scripts`
  2.`activate`
- 此时可查看到一个克隆本地电脑的干净Python环境
`pip list` (查看当前虚拟环境安装的Python包)

- 退出虚拟环境
`deactivate`

#### 注：操作均为在虚拟环境下进行

- 安装好所需扩展包后进行requirements.txt文件的生成动作
`pip freeze >requirements.txt`
(此文件用于记录所有依赖包及其精确的版本号。以便新环境部署。)

- 之后生成新的虚拟环境可通过
`pip install -r requirements.txt`
(即可一键安装所需依赖包)

#### 使用Flask-Migrate实现数据库的迁移，可用于创建以及更新表的操作，之后无需手动创建表结构。

1.`python manage.py db init` (创建迁移仓库)

2.`python manage.py db migrate -m "initial migration"`(创建迁移脚本，需先创建改数据库不然会报改数据库不存在)

3.`python manage.py db upgrade`(更新数据库)
- 至此数据库已生成所需表结构

- 如变更表结构需要删除数据表与版本控制表再执行2，3的动作
- 已有迁移脚本只需执行3动作即可生成表结构

- 测试路由
    - 获取验证码路由(浏览器访问)
    `http://localhost:5000/fumei/users/getaliyuncode?phone=18579209598`
    - 登录路由(以下均为curl访问)
    `curl -d "phone=18579209598&pwd=88888888&code=312804" 127.0.0.1:5000/fumei/users/login -X POST`
    - 注册路由
    `curl -d "phone=13627007061&pwd=88888888&code=182973" 127.0.0.1:5000/fumei/users/register -X POST`
    - 修改密码
    `curl -d "phone=13879266523&pwd=88888&code=809745" 127.0.0.1:5000/fumei/users/changepassword -X POST`
    - 上市人
    
    
