import time
from models import Model


class Theme(Model):
    def __init__(self, form):
        self.id = None
        self.name = form.get('name', '')
        self.type = self.__class__.__name__
        self.ct = int(time.time())
        self.ut = self.ct
        self.topic_num = 0
        self.board_id = int(form.get('board_id', -1))
        self.user_id = int(form.get('user_id', -1))
        self.user_name = form.get('user_name', '')
        self.banner_img = 'default.png'
