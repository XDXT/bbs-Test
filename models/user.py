from models.mongxa import Mongxa


class User(Mongxa):
    __fields__ = Mongxa.__fields__ + [
        ('username', str, ''),
        ('password', str, ''),
        ('role', int, -1),
        ('user_image', str, ''),
        ('active_id', str, ''),
    ]

    """
    User 是一个保存用户数据的 model
    属性 username ,password, user_image, role, active_id
    """

    def __init__(self):
        self.user_image = 'default.png'
        self.role = 10

    def salted_password(self, password, salt='$!@><?>HUI&DWQa`'):
        import hashlib
        def sha256(ascii_str):
            return hashlib.sha256(ascii_str.encode('ascii')).hexdigest()

        hash1 = sha256(password)
        hash2 = sha256(hash1 + salt)
        return hash2

    def hashed_password(self, pwd):
        import hashlib
        p = pwd.encode('ascii')
        s = hashlib.sha256(p)
        return s.hexdigest()

    @classmethod
    def validate_username(cls, form):
        username = form.get("username", '')
        user = User.find_by(username=username)
        if user is not None or username is '':
            return False
        else:
            return True

    @classmethod
    def register(cls, form):
        name = form.get('username', '')
        pwd = form.get('password', '')
        if len(name) > 2 and User.find_by(username=name) is None:
            u = User.new(form)
            u.password = u.salted_password(pwd)
            u.save()
            return u
        else:
            return None

    @classmethod
    def validate_login(cls, form):
        u = User()
        u.username = form.get("username", '')
        u.password = form.get("password", "")
        user = User.find_by(username=u.username)
        if user is not None and user.password == u.salted_password(u.password):
            return user
        else:
            return None
