import time
from models.mongxa import Mongxa


class Reply(Mongxa):
    __fields__ = Mongxa.__fields__ + [
        ('content', str, ''),
        ('topic_id', int, -1),
        ('user_id', int, -1),
    ]

    def user(self):
        from .user import User
        u = User.find(self.user_id)
        return u
