import os
import time


def log(*args, **kwargs):
    # time.time() 返回 unix time
    # 如何把 unix time 转换为普通人类可以看懂的格式呢？
    format = '%H:%M:%S'
    value = time.localtime(int(time.time()))
    dt = time.strftime(format, value)
    with open('log.bbs.txt', 'a', encoding='utf-8') as f:
        print(dt, *args, file=f, **kwargs)


def delete_file(file_director, filename):
    path = os.path.join(file_director, filename)
    if os.path.exists(path):
        try:
            os.remove(path)
            log("delete file: {}".format(path))
        except OSError:
            log("It's not a file ,it's a director: {}".format(path))
    else:
        log('no such file: {}'.format(path))
