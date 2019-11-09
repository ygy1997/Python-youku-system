import hashlib
import json
import struct
import uuid
from functools import wraps
from db import user_data


def get_md5(pwd):
    md5 = hashlib.md5()
    md5.update(pwd.encode('utf-8'))
    sal = '16岁的tank'
    md5.update(sal.encode('utf-8'))
    return md5.hexdigest()





# 随机加密字符串
def get_session(username):
    md5 = hashlib.md5()
    md5.update(username.encode('utf-8'))
    uuid_obj = uuid.uuid4()
    md5.update(str(uuid_obj).encode('utf-8'))
    return md5.hexdigest()


# 登录认证
def login_auth(func):

    @wraps(func)
    def inner(*args, **kwargs):  # args == (back_dic, conn)
        # 登录拦截
        # 服务端所有的session: user_data.online_user  # {'addr': [session, id]}
        # 获取客户端的session值
        back_dic = args[0]
        session = back_dic.get('session')
        # 获取客户的addr值
        addr = back_dic.get('addr')
        user_data.mutex.acquire()
        # 获取服务端对应的用户session与id值
        session_id = user_data.online_user.get(addr)  # [session, id]
        user_data.mutex.release()
        # 校验客户端的session与服务端的session是否一致
        if session_id:
            if session_id[0] == session:

                # 获取用户的id，以便后期使用
                # back_dic == args[0]
                args[0]['user_id'] = session_id[1]

                res = func(*args, **kwargs)
                return res
        else:
            send_dic = {'flag': False, 'msg': '请先登录!'}
            return send_dic
        # send_msg(send_dic, args[1])  # args[1] == conn

    return inner



