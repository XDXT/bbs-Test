from flask import (
    render_template,
    request,
    redirect,
    url_for,
    Blueprint,
    send_from_directory,
)

from routes import (
    current_user,
    file_exists,
    allow_save,
    join_director,
)

from utils import delete_file

from models.topic import Topic
from models.theme import Theme
from models.reply import Reply
from config import image_file_director
import json

local_image_director = join_director(image_file_director, 'topic')

main = Blueprint('topic', __name__)


@main.route("/")
def index():
    return redirect(url_for('theme.index'))


@main.route('/<int:id>')
def detail(id):
    m = Topic.get(id)
    r = Reply.find_all(topic_id=m.id)
    return render_template("topic/detail.html", topic=m, replies=r)


@main.route("/add", methods=["POST"])
def add():
    u = current_user()
    user_info = {
        'user_id': u.id,
        'user_name': u.username,
    }

    if file_exists():
        print('file=', request.files)
        return redirect(url_for('topic.new', tip='no name/theme img'))

    filename = allow_save(local_image_director)
    if filename is not None:
        form = request.form
        m = Topic.new(form, **user_info)
        m.banner_img = filename
        m.content = form.get('content', '')
        m.save()
        t = Theme.find(m.theme_id)
        t.topic_num += 1
        t.save()
    return redirect(url_for('theme.index'))


@main.route("/add_ckimg", methods=["POST"])
def add_ckimg():
    if file_exists('upload'):
        print('file_exists')
        return redirect(url_for('topic.new', tip='no name/file'))

    filename = allow_save(local_image_director, 'upload')
    imgurl = 'http://nuclearcat.xyz' + url_for('topic.downloads', filename=filename)
    cj = {
        'default': '840',
        'url': imgurl,
    }
    # res = make_response(json.dumps(cj,ensure_ascii=False))
    # res.headers['Access-Control-Allow-Origin'] = 'http://www.nuclearcat.xyz'
    return json.dumps(cj, ensure_ascii=False)


@main.route("/new")
def new():
    bs = Theme.all()
    tip = request.args.get('tip', 'none')
    return render_template("topic/new.html", bs=bs, tip=tip)


@main.route("/delete")
def delete():
    # TODO token与用户验证
    topic_id = int(request.args.get('id'))
    tp = Topic.find(topic_id)
    print('删除 的 topic 是', tp)
    t = Theme.find(tp.theme_id)
    t.topic_num -= 1
    t.save()
    delete_file(local_image_director, tp.banner_img)
    tp.delete()
    return redirect(url_for('theme.detail'))


@main.route("/uploads/<filename>")
def downloads(filename):
    return send_from_directory(local_image_director, filename)
