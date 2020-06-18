from flask import (
    render_template,
    request,
    redirect,
    session,
    url_for,
    Blueprint,
    make_response,
    send_from_directory,
)

from routes import (
    is_login,
    current_user,
    file_exists,
    allow_save,
    join_director,
)

from config import image_file_director

local_image_director = join_director(image_file_director, 'user_head')


main = Blueprint('user', __name__)


@main.route("/")
@is_login
def index():
    u = current_user()
    return render_template("/user/info.html", user=u)


@main.route('/addimg', methods=["POST"])
def add_img():
    u = current_user()

    if file_exists():
        return redirect(url_for('board.new', tip='no name/file'))

    filename = allow_save(local_image_director)
    if filename is not None:
        u.user_image = filename
        u.save()

    return redirect(url_for(".index"))


@main.route("/uploads/<filename>")
def downloads(filename):
    return send_from_directory(local_image_director, filename)


@main.route("/downloads/<filename>")
def upload_head(filename):
    return send_from_directory(local_image_director, filename)
