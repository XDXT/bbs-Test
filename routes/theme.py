from flask import (
    render_template,
    request,
    redirect,
    url_for,
    Blueprint,
    send_from_directory,
    abort,
)

from routes import (
    get_token,
    flash_token,
    current_user,
    file_exists,
    allow_save,
    join_director,
)

from utils import (
    log,
    delete_file,
)

from models.topic import Topic
from models.theme import Theme
from models.board import Board
from config import image_file_director
import math

local_image_director = join_director(image_file_director, 'main_banner')

main = Blueprint('theme', __name__)


@main.route("/")
def index():
    bs = Board.all()
    te_top = []
    te_centers = []
    te_top.append(bs[0])
    te_top.append(Theme.find_all(board_id=bs[0].id))
    for i, b in enumerate(bs):
        if i > 0:
            temp = []
            themes = Theme.find_all(board_id=b.id)
            temp.append(b)
            temp.append(themes)
            te_centers.append(temp)
    return render_template("theme/index.html", te_top=te_top, te_centers=te_centers)


def check_idpage(id_page):
    if id_page.split('-')[0] is id_page:
        id_page += '-1'
    if id_page.split('-')[1] is '':
        id_page += '1'
    pageinfo = tuple([int(i) for i in id_page.split('-')])
    return pageinfo


@main.route('/<id_page>')
def detail(id_page):
    topic_num = 5
    (id, page) = check_idpage(id_page)
    (startn, endn) = ((page-1)*topic_num, page*topic_num)
    m = Theme.find(id)
    pages = math.ceil(m.topic_num / topic_num)
    if m.topic_num < startn or startn < 0:
        abort(404)
    elif startn < m.topic_num < endn:
        tps = Topic.find_all(theme_id=m.id)[startn:]
        # tps = Topic.cache_all()
    else:
        tps = Topic.find_all(theme_id=m.id)[startn: endn]
    return render_template("theme/detail.html", theme=m, tps=tps, pgs=pages)


@main.route("/add", methods=["POST"])
def add():
    u = current_user()
    if file_exists():
        return redirect(url_for('board.new', tip='no name/file'))

    filename = allow_save(local_image_director)
    if filename is not None:
        form = request.form
        m = Theme.new(form, user_id=u.id, user_name=u.username)
        m.banner_img = filename
        m.save()

    return redirect(url_for('board.new', tip='success'))


@main.route("/delete")
def delete():
    id = int(request.args.get('id'))
    token = request.args.get('token')
    u = current_user()
    t = get_token(u.id)
    if t.content == token:
        flash_token(t)
        b = Theme.find(id)
        log('删除 theme 用户是', u, b)
        delete_file(local_image_director, b.banner_img)
        Theme.delete(id)
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
        flash_token(t)
        b = Theme.find(id)
        log('update board 用户是', u.id, u.username, b)
        b.name = name
        b.save()
        return redirect(url_for('board.edit'))
    else:
        abort(403)


@main.route("/uploads/<filename>")
def downloads(filename):
    return send_from_directory(local_image_director, filename)


