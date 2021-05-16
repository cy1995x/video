import hashlib
from time import time


def md5_token(name):
    ctime = str(time())
    m = hashlib.md5(name.encode('utf-8'))
    m.update(ctime.encode('utf-8'))
    return m.hexdigest()


def md5_pwd(pwd):
    m = hashlib.md5()
    m.update(pwd.encode('utf-8'))
    return m.hexdigest()
