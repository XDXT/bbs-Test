from flask import (
    redirect,
    request,
    session,
    url_for,
    abort,
)

import os
import uuid
import time
from werkzeug.utils import secure_filename
# from utils import log
from models.user import User
from models.token import Token


def current_user():
    uai = session.get('user_active_id', 'None')
    u = User.find_by(active_id=uai)
    return u


def flash_token(token):
    if len_time(token) > 600:
        token.updated_time = int(time.time())
        token.content = str(uuid.uuid4())
        token.save()
    return token


def get_token(uid):
    token = Token.find_by(user_id=uid)
    if token is None:
        token = Token.new({}, user_id=uid)
    token = flash_token(token)
    return token


def len_time(obj):
    lg = int(time.time()) - obj.updated_time
    return lg


def is_login(view_func):
    from functools import wraps
    @wraps(view_func)
    def check_login(*args, **kwargs):
        u = current_user()
        if u is None:
            return redirect(url_for('index.login_page'))
        else:
            return view_func(*args, **kwargs)

    return check_login


def is_admin(view_func):
    from functools import wraps
    @wraps(view_func)
    def check_role(*args, **kwargs):
        u = current_user()
        if u is None:
            return redirect(url_for('index.login_page'))
        if u.role != 1:
            abort(403)
        else:
            return view_func(*args, **kwargs)

    return check_role


def check_role(role):
    u = current_user()
    if u is None:
        return False

    if u.role > role:
        return False
    else:
        return True


def file_exists(allow_name='file'):
    if allow_name not in request.files:
        return True

    file = request.files[allow_name]
    if file.filename == '':
        return True

    return False


def allow_file(filename):
    suffix = filename.split('.')[-1]
    from config import accept_user_file_type
    return suffix in accept_user_file_type


def join_director(director, filename):
    d = os.path.join(director, filename)
    return d


def allow_save(file_director, allow_name='file'):
    file = request.files[allow_name]
    if allow_file(file.filename):
        fname = secure_filename(file.filename).split('.')
        newname = str(uuid.uuid4()).replace('-', '') + '_' + fname[-2]
        filename = newname + '.' + fname[-1]
        file.save(os.path.join(file_director, filename))
    else:
        filename = 'default.png'
    return filename
