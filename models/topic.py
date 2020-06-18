import time
import json
from models.mongxa import Mongxa
from models.redisxa import RedisCache


class Topic(Mongxa):
    __fields__ = Mongxa.__fields__ + [
        ('views', int, -1),
        ('title', str, ''),
        ('content', str, ''),
        ('user_id', int, -1),
        ('user_name', str, ''),
        ('theme_id', int, ''),
        ('banner_img', str, ''),
    ]

    def __init__(self):
        self.banner_img = 'default.png'
        self.views = 0

    should_update = True  # type: bool
    redis_cache = RedisCache()

    @classmethod
    def cache_all(cls):
        if cls.should_update:
            fields = Topic.__fields__
            cls.redis_cache.set('topic_all', json.dumps([cls.redis_cache.to_json(fields, i) for i in cls.all()]))
            cls.should_update = False
        j = json.loads(cls.redis_cache.get('topic_all').decode('utf-8'))
        j = [cls.redis_cache.from_json(cls(), i) for i in j]
        return j

    def save(self):
        should_update = True  # type: bool
        super().save()  # type: mongxa.save

    def replies(self):
        from .reply import Reply
        ms = Reply.find_all(topic_id=self.id)  # type: List(Reply)
        return ms

    def get_board(self):
        from .board import Board
        b = Board.find(self.board_id)  # type: Board
        return b
