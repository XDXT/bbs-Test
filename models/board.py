import time
from models import Model


class Board(Model):
    def __init__(self, form):
        self.id = None
        self.name = form.get('name', '')
        self.type = self.__class__.__name__
        self.ct = int(time.time())
        self.ut = self.ct
        self.banner_img = 'default.png'

