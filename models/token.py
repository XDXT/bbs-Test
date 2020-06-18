import uuid
from models.mongxa import Mongxa


class Token(Mongxa):
    __fields__ = Mongxa.__fields__ + [
        ('content', str, ''),
        ('user_id', int, -1),
    ]

    def __init__(self):
        self.content = str(uuid.uuid4())
