import datetime
import os

from orm.models import Notice, User, DownloadRecord, Movie
from lib import common

from conf import settings

@common.login_auth
def check_dowload_record_interface(back_dic):
    record_obj_list = DownloadRecord().select(
        "user_id = {}".format(back_dic.get('id')))

    # 获取当前用户的下载的电影名称
    movie_list = []

    for record_obj in record_obj_list:
        movie_id = record_obj.movie_id
        movie_obj = Movie().select(whereStr="id = {}".format(movie_id))[0]
        movie_list.append(
            [movie_obj.name, str(record_obj.download_time)]
        )

    send_dic = {
        'flag': True,
        'movie_list': movie_list
    }

    return send_dic
@common.login_auth
def download_movie_interface(back_dic,):
    movie_path = os.path.join(
        settings.DOWNLOAD_MOVIES_PATH,
        back_dic.get('movie_name')
    )

    # 获取电影大小
    movie_size = os.path.getsize(movie_path)

    # 若当前下载用户不是会员，设置40秒广告时间
    wait_time = 0

    is_vip = back_dic.get('is_vip')

    if not is_vip:
        wait_time = 2

    send_dic = {
        'flag': True,
        'movie_size': movie_size,
        'wait_time': wait_time,
        'movie_path' :movie_path
    }
    record_obj = DownloadRecord(
        user_id=back_dic.get('id'),
        movie_id=back_dic.get('movie_id'),
        download_time=str(datetime.datetime.now())
    )

    record_obj.save()
    return send_dic
@common.login_auth
def buy_vip_interface(back_dic,):
    username = back_dic.get('username')
    user_obj = User().select(whereStr="name = '{}'".format(username))
    if user_obj:
        user_obj[0].is_vip = 1
        user_obj[0].update()
        send_dic = {
            'msg': '购买成功，会员爸爸!'
        }
    else:
        send_dic = {
            'msg': '操作失败!'
        }
    return send_dic
@common.login_auth
def check_notice_interface(back_dic,):
    notice_obj_list = Notice().select()
    if notice_obj_list:
        notice_list = []

        for notice_obj in notice_obj_list:
            notice_list.append(
                # [公告标题，内容]
                [notice_obj.title, notice_obj.content]
            )

        send_dic = {
            'flag': True,
            'notice_list': notice_list,
            'msg':'查看公告成功'
        }
    else:
        send_dic = {
            'flag': False,
            'msg': '没有公告'
        }
    return send_dic
