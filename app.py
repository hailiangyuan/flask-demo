# coding=utf-8
from flask import Flask, render_template, session, redirect, \
    url_for, flash, current_app, request
from flask_script import Manager
from flask_login import UserMixin, LoginManager, login_required
from wtforms.validators import DataRequired
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, \
    BooleanField, IntegerField, ValidationError
from wtforms.validators import Required, Length, Regexp
import time
# 自定义 方法
from MyHttpUtil import MyUtil

'''
Config
'''

app = Flask(__name__)
app.debug = True
manager = Manager(app)
app.config['SECRET_KEY'] = "this is a secret_key"
bootstrap = Bootstrap(app)
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'login'
login_manager.login_message = u"你需要登录才能访问这个页面."
login_manager.init_app(app)
'''
使用者bean
'''


class User(UserMixin):
    pass

    def get_id(self):
        return 123

    def __init__(self, username):
        self.username = username
        self.id = self.get_id()

    @staticmethod
    def verify_password(password):
        pwd = time.strftime("%Y%m%d", time.localtime())
        print("用户输入的pwd:" + password)
        print("随机的pwd:" + pwd)
        return pwd == password
    #
    # def get_name(self, user_id):
    #     if len(user_id) > 0:
    #         return self.name
    #     else:
    #         return "Admin"


'''
定时任务bean
'''


class Corn(object):

    def __init__(self, new_imei, new_corn):
        # 新添加的用户，初始其角色为任务。
        self.IMEI = new_imei
        self.CORN = new_corn

    def get_imei(self):
        return self.IMEI

    def get_corn(self):
        return self.CORN


'''
Forms
'''


class LoginForm(FlaskForm):
    number = StringField(u'用户名', validators=[DataRequired()])
    password = PasswordField(u'密码', validators=[DataRequired()])
    # remember_me = BooleanField(u'记住我')
    submit = SubmitField(u'登录')


class CornListForm(object):
    def test(self):
        lists = MyUtil.corn_list()
        corn_list = []
        for str_corn in lists:
            print("Corns:" + str(str_corn['imei']) + str(str_corn['corn']))
            i = Corn(new_imei=str_corn['imei'], new_corn=str_corn['corn'])
            corn_list.append(i)
        print(corn_list)
        Corns = corn_list


class SearchForm(FlaskForm):
    number = StringField(u'imei', validators=[DataRequired(message=u'请输入数字')])
    submit = SubmitField(u'搜索')


class CornAddForm(FlaskForm):
    Cornname = StringField(u'IMEI', validators=[DataRequired()])
    number = StringField(u'CORN', validators=[DataRequired(message=u'请输入corn')])
    submit = SubmitField(u'添加')


class CornEditForm(FlaskForm):
    imei = IntegerField(u'imei', validators=[DataRequired()])
    corn = StringField(u'corn', validators=[DataRequired(message=u'请输入数字')])
    submit = SubmitField(u'提交修改')


'''
views
'''


@app.route('/', methods=['GET', 'POST'])
@login_required
def first():
    return render_template('login.html', form=LoginForm())


@app.route('/index', methods=['GET', 'POST'])
def index():
    lists = MyUtil.corn_list()
    corn_list = []
    for str_corn in lists:
        print("Corns:" + str(str_corn['imei']) + str(str_corn['corn']))
        i = Corn(new_imei=str_corn['imei'], new_corn=str_corn['corn'])
        corn_list.append(i)
    print(corn_list)
    Corns = corn_list
    form = SearchForm()
    # print(form)
    return render_template('index.html', form=form, Corns=Corns)


# 增加新CORN
@app.route('/add-Corn', methods=['GET', 'POST'])
# @login_required
def add_corn():

    form = CornAddForm()
    if form.validate_on_submit():
        MyUtil.corn_add(form.Cornname.data, form.number.data)
        flash(u'成功添加CORN')
        return redirect(url_for('index'))

    return render_template('add_user.html', form=form)


# 删除CORN
@app.route('/remove-Corn/<int:id>', methods=['GET', 'POST'])
# @login_required
def remove_corn(id):
    if MyUtil.corn_delete(id):
        flash(u'删除成功')
    else:
        flash(u'删除失败')
    return redirect(url_for('index'))


# 修改CORN资料
@app.route('/edit-Corn/<int:id>', methods=['GET', 'POST'])
# @login_required
def edit_corn(id):
    # 先查出来
    old_corn = MyUtil.corn_find(id)
    print("old_corn:"+str(old_corn))
    form = CornEditForm()
    if form.validate_on_submit():
        Cornname = form.imei.data
        number = form.corn.data
        MyUtil.corn_updete(Cornname, number)
        flash(u'信息已更改')
        return redirect(url_for('index'))
    form.imei.data = old_corn['imei']
    form.corn.data = old_corn['corn']
    return render_template('edit_user.html', form=form)
    # print("出错了！")
    # form.Cornname.data = Corn.get_imei()
    # form.number.data = Corn.number
    # return render_template('edit_user.html', form=form, Corn=Corn)


# 登录，系统只允许管理员登录
@app.route('/login', methods=['GET', 'POST'])
def login():
    flash(u'login...')
    form = LoginForm()
    if form.validate_on_submit():
        num = form.number.data
        pwd = form.password.data
        print("pwd:" + pwd)
        flag = User.verify_password(password=pwd)
        if flag:
            flash(u'登录成功！')
            return redirect(url_for('index'))
        else:
            flash(u'用户名或密码错误！请联系管理员！')
    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    # logout_Corn()
    flash(u'成功注销！')
    return redirect(url_for('login'))


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


# 加载用户的回调函数
@login_manager.user_loader
def load_user(user_id):
    # if user_id is None:
    #     return redirect(url_for('login'))
    # return User.get_name(user_id)
    if user_id is not None:
        curr_user = User("test")
        curr_user.id = user_id
    else:
        curr_user = User("test")
        curr_user.id = 123
        return curr_user


# @login_manager.user_loader
# def load_user(user_id):
#     return User.get_id(user_id)

'''
增加命令'python app.py init' 
以增加身份与初始管理员帐号
'''

#
# @manager.command
# def init():
#     from app import User
#     Role.insert_roles()
#     Corn.generate_admin()


if __name__ == '__main__':
    app.run(debug=True)
    manager.run()
