import time
from pymongo import MongoClient
monga = MongoClient()
# monga 就是client

def timestamp():
    return int(time.time())


def next_id(name):
    query = {
        'name': name,
    }
    update = {
        '$inc': {
            'seq': 1
        }
    }
    kwargs = {
        'query': query,
        'update': update,
        'upsert': True,
        'new': True,
    }
    # 存储数据的 id
    doc = monga.db['data_id']
    # find_and_modify 是一个原子操作函数
    new_id = doc.find_and_modify(**kwargs).get('seq')
    return new_id


class Mongxa(object):
    __fields__ = [
        '_id',
        # (字段名, 类型, 值)
        ('id', int, -1),
        ('type', str, ''),
        ('deleted', bool, False),
        ('created_time', int, 0),
        ('updated_time', int, 0),
    ]

    @classmethod
    def has(cls, **kwargs):
        """
        检查一个元素是否在数据库中 用法如下
        User.has(id=1)
        :param kwargs:
        :return:
        """
        return cls.find_one(**kwargs) is not None

    def mongos(self, name):
        return monga.db[name]._find()

    def __repr__(self):
        class_name = self.__class__.__name__
        properties = ('{0} = {1}'.format(k, v) for k, v in self.__dict__.items())
        return '<{0}: \n  {1}\n>'.format(class_name, '\n  '.join(properties))

    @classmethod
    def new(cls, form=None, **kwargs):
        # new 是给外部使用的函数
        name = cls.__name__
        # 创建一个空对象
        m = cls()
        dm = m.__dict__
        # 把定义的数据写入空对象, 未定义的数据输出错误
        fields = cls.__fields__.copy()
        # 去掉 _id 这个特殊的字段
        fields.remove('_id')
        if form is None:
            form = {}

        for f in fields:
            # f  (id, int, 1)
            k, t, v = f
            if k in dm:
                continue
            elif k in form:
                setattr(m, k, t(form[k]))
            else:
                # 设置默认值
                setattr(m, k, v)
        # 处理额外的参数 kwargs
        for k, v in kwargs.items():
            if hasattr(m, k):
                setattr(m, k, v)
            else:
                raise KeyError
        # 写入默认数据
        m.id = next_id(name)
        ts = int(time.time())
        m.created_time = ts
        m.updated_time = ts
        # m.deleted = False
        m.type = name.lower()
        # 特殊 model 的自定义设置
        # m._setup(form)
        m.save()
        return m

    @classmethod
    def _new_with_bson(cls, bson):
        """
        这是给内部 all 这种函数使用的函数
        从 mongo 数据中恢复一个 model
        """
        m = cls()
        fields = cls.__fields__.copy()
        # 去掉 _id 这个特殊的字段
        fields.remove('_id')
        for f in fields:
            # (k, t, v) = (字段名 id, 类型 int, 值 1)
            k, t, v = f
            if k in bson:
                setattr(m, k, bson[k])
            else:
                # 设置默认值
                setattr(m, k, v)
        setattr(m, '_id', bson['_id'])
        return m

    @classmethod
    def all(cls):
        # 按照 id 升序排序
        return cls._find()

    @classmethod
    def _find(cls, **kwargs):
        """
        mongo 数据查询
        """
        name = cls.__name__
        flag_sort = '__sort'
        sort = kwargs.pop(flag_sort, None)
        ds = monga.db[name].find(kwargs)
        if sort is not None:
            ds = ds.sort(sort)
        l = [cls._new_with_bson(d) for d in ds if d['deleted'] is False]
        return l

    @classmethod
    def _find_raw(cls, **kwargs):
        name = cls.__name__
        ds = monga.db[name]._find(kwargs)
        l = [d for d in ds]
        return l

    @classmethod
    def _clean_field(cls, source, target):
        """
        清洗数据用的函数
        例如 User._clean_field('is_hidden', 'deleted')
        把 is_hidden 字段全部复制为 deleted 字段
        """
        ms = cls._find()
        for m in ms:
            v = getattr(m, source)
            setattr(m, target, v)
            m.save()

    @classmethod
    def find_by(cls, **kwargs):
        return cls.find_one(**kwargs)

    @classmethod
    def find_all(cls, **kwargs):
        return cls._find(**kwargs)

    @classmethod
    def find(cls, id):
        return cls.find_one(id=id)

    @classmethod
    def get(cls, id):
        return cls.find_one(id=id)

    @classmethod
    def find_one(cls, **kwargs):
        l = cls._find(**kwargs)
        if len(l) > 0:
            return l[0]
        else:
            return None

    @classmethod
    def upsert(cls, query_form, update_form, hard=False):
        ms = cls.find_one(**query_form)
        if ms is None:
            query_form.update(**update_form)
            ms = cls.new(query_form)
        else:
            ms.update(update_form, hard=hard)
        return ms

    def update(self, form, hard=False):
        for k, v in form.items():
            if hard or hasattr(self, k):
                setattr(self, k, v)
        self.save()

    def save(self):
        name = self.__class__.__name__
        monga.db[name].save(self.__dict__)

    def delete(self):
        name = self.__class__.__name__
        query = {
            'id': self.id,
        }
        # 多设一个deleted属性代替真实删除
        # values = {
        #     'deleted': True
        # }
        # # self.deleted = True
        # # self.save()
        # monga.db[name].update_one(query, values)

        monga.db[name].remove(query)

    def blacklist(self):
        b = [
            '_id',
        ]
        return b

    def json(self):
        _dict = self.__dict__
        d = {k: v for k, v in _dict.items() if k not in self.blacklist()}
        return d

    def part_json(self, *args):
        _dict = self.__dict__
        d = {k: v for k, v in _dict.items() if k not in self.blacklist() and k in args}
        return d

    def data_count(self, cls):
        """
        查看用户发表的评论数
        u.data_count(Comment)
        :return: int
        """
        name = cls.__name__
        fk = '{}_id'.format(self.__class__.__name__.lower())
        query = {
            fk: self.id,
        }
        count = monga.db[name]._find(query).count()
        return count
