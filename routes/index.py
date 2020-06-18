from flask import (
    render_template,
    request,
    redirect,
    session,
    url_for,
    Blueprint,
)

from routes import (
    is_login,
    is_admin,
)


import json
import time
from models.user import User
from models.notice import Notice

main = Blueprint('index', __name__)


"""
用户在这里可以
    访问首页
    注册
    登录

用户登录后, 会写入 session, 并且定向到 /index
"""


@main.route("/")
def index():
    return render_template("index.html")

@main.route("/admin")
@is_admin
def admin():
    return render_template("admin.html")

@main.route('/notice/content')
def notice():
    # return 一个最新公告内容json
    note = Notice.find(id=1)
    return json.dumps(note.content, ensure_ascii=False)


@main.route('/notice/new')
def new_notice():
    # Todo 权限与安全
    note = Notice.find(id=1)
    if note is None:
        note = Notice.new({})
    return render_template("notice/new.html", note=note)


@main.route('/notice/add', methods=["POST"])
def add_notice():
    # Todo 权限与安全
    form = request.form
    note = Notice.find(id=1)
    note.name = form.get('name', '')
    note.content = form.get('content', '')
    note.save()
    return redirect(url_for('.new_notice'))


@main.route('/login_page')
def login_page():
    tip = request.args.get('tip', 'none')
    return render_template('login.html', tip=tip)


@main.route('/testpart')
@is_login
def testpart():
    tip = request.args.get('tip', 'none')
    return render_template('testpart.html', tip=tip)


@main.route('/test_func', methods=["POST"])
def test_func():
    pass


@main.route("/register", methods=['POST'])
def register():
    form = request.form
    if User.validate_username(form):
        User.register(form)
        return redirect(url_for('.login_page', tip='register success'))
    else:
        return redirect(url_for('.login_page', tip='User name has been used'))


@main.route("/login", methods=['POST'])
def login():
    form = request.form
    u = User.validate_login(form)
    if u is None:
        return redirect(url_for('.login_page', tip='name or passwoar erro'))
    else:
        u.active_id = 'abc' + str(time.time()) + str(u.id)
        u.save()
        session['user_active_id'] = u.active_id
        # 设置 cookie 有效期为 永久
        session.permanent = True
        # 删除cookies
        # session.pop('user_id')
        return redirect(url_for('theme.index'))
