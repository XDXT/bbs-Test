import time
from models import Model


class Notice(Model):
    def __init__(self, form):
        self.id = None
        self.name = form.get('name', '')
        self.content = form.get('content', '')
        self.type = self.__class__.__name__
        self.ct = int(time.time())
        self.ut = self.ct
