import datetime
from threading import Lock

from db import user_data
from lib import common
from orm.models import User, Movie

lock = Lock()

lock.acquire()
user_data.mutex = lock
lock.release()


def register_interface(back_dic,):

    # 面条版: 业务逻辑
    username = back_dic.get('username')

    user_obj = User(name=username).select(whereStr ="name = {}".format(username))

    if not user_obj:
        password = back_dic.get('password')

        # 创建数据
        user_obj = User(name=username,
                       password=common.get_md5(password),
                       user_type=back_dic.get('user_type'),
                       register_time=str(datetime.datetime.now()),
                       is_vip=0,
                       is_locked=0
                       )
        user_obj.save()

        send_dic = {
            'flag': True,
            'msg': '注册成功!'
        }
    else:
        send_dic = {'flag': False,
                    'msg': '用户已存在!'}
    return send_dic


def login_interface(back_dic,):
    username = back_dic.get('username')
    usertype = back_dic.get('user_type')
    # 判断用户是否存在
    user_list = User(name=username).select(whereStr ="name = {} and user_type = '{}' ".format(username,str(usertype)))

    if user_list:
        user_obj = user_list[0]
        password = back_dic.get('password')
        # 判断密码是否正确
        if common.get_md5(password) == user_obj.password:

            # 登录成功后记录状态
            # cookies， session
            # 一个加密后的随机字符串
            session = common.get_session(username)

            addr = back_dic.get('addr')

            # 保存session到服务端
            # [session, user_obj.user_id]  # [afwagawgwaawgwaga, 1]
            # 把用户session字符串与id写入user_data文件中
            # user_data.mutex.acquire()
            user_data.online_user[addr] = [session, user_obj.id]
            # user_data.mutex.release()

            send_dic = {
                'flag': True,
                'msg': '登录成功',
                'id': user_obj.id,
                'session': session,
                'is_vip': user_obj.is_vip
            }
        else:
            send_dic = {
                'flag': False,
                'msg': '密码错误'
            }
    else:
        send_dic = {
            'flag': False,
            'msg': '用户不存在!'
        }
    return send_dic

@common.login_auth
def check_movie_interface(back_dic):

    movie_md5 = back_dic.get('movie_md5')

    movie_list = Movie(file_md5=movie_md5).select(whereStr="file_md5='{}'".format(movie_md5))

    if movie_list:
        if movie_list[0].is_delete == 0:
            send_dic = {'flag': False,
                    'msg': '电影已存在!'}
        else:
            movie_list[0].is_delete = 0
            movie_list[0].update()
            send_dic = {
                'flag': False,
                'msg': '文件已经存在，恢复成功'
            }
    else:
        send_dic = {
            'flag': True,
            'msg': '可以上传'
        }

    return send_dic

@common.login_auth
def get_movie_list_interface(back_dic):

    movie_list = Movie().select(whereStr="is_delete = 0")
    back_movie_list = []
    # 若没有未删除的电影
    if not movie_list:

        send_dic = {
            'flag': False,
            'msg': '没有电影'
        }
    # 有可删除的电影
    else:
        for movie_obj in movie_list:

            if back_dic.get('movie_type') == 'all':
                back_movie_list.append(
                    [movie_obj.name,
                     '免费' if movie_obj.is_free else '收费',
                     movie_obj.id
                     ]  # 电影的名字、是否免费、电影id
                )

            # 作业1: 获取收费电影
            elif back_dic.get('movie_type') == 'free':
                # 判断如果是免费电影
                if movie_obj.is_free:
                    back_movie_list.append(
                        [movie_obj.name,
                         '免费',
                         movie_obj.id
                         ]  # 电影的名字、免费、电影id
                    )

            # 作业2: 获取免费电影
            else:
                if not movie_obj.is_free:
                    back_movie_list.append(
                        [movie_obj.name,
                         '收费',
                         movie_obj.id]
                    )

        send_dic = {
            'flag': True,
            'movie_list': back_movie_list
        }
    return send_dic
