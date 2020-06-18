from flask import (
    render_template,
    request,
    redirect,
    url_for,
    Blueprint,
    sessions,
    abort,
)

from routes import (
    is_admin,
    get_token,
    flash_token,
    current_user,
    join_director,
)

from utils import (
    log,
    delete_file,
)

from models.board import Board
from models.theme import Theme
from models.token import Token
from config import image_file_director

local_image_director = join_director(image_file_director, 'main_banner')


main = Blueprint('board', __name__)


@main.route("/new")
@is_admin
def new():
    tip = request.args.get('tip', 'none')
    bs = Board.all()
    return render_template("/board/new.html", bs=bs, tip=tip)


@main.route("/edit")
@is_admin
def edit():
    u = current_user()
    token = get_token(u.id)
    bs = Board.all()
    ts = Theme.all()
    return render_template("/board/forum_edit.html", bs=bs, ts=ts, token=token.content)


# todo is_login要做成is_admin
@main.route("/add", methods=["POST"])
def add():
    form = request.form
    Board.new(form)
    return redirect(url_for('.new'))


@main.route("/delete")
def delete():
    id = int(request.args.get('id'))
    token = request.args.get('token')
    u = current_user()
    t = get_token(u.id)
    if t.content == token:
        flash_token(t)
        b = Board.find(id)
        log('删除 board 用户是', u, b)
        delete_file(local_image_director, b.banner_img)
        Board.delete(id)
        return redirect(url_for('board.edit'))
    else:
        abort(403)


@main.route("/update", methods=["POST"])
def update():
    token = request.args.get('token')
    form = request.form
    id = int(form.get('id', -1))
    name = form.get('name', '')
    u = current_user()
    t = get_token(u.id)
    if t.content == token and '' != name:
        b = Board.find(id)
        log('update board 用户是', u.id, u.username, b)
        b.name = name
        b.save()
        return redirect(url_for('board.edit'))
    else:
        abort(403)
