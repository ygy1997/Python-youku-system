import datetime

import os
import socket

user_info = {
    'cookies': None
}

from conf import settings
from lib import common
from orm import models

#上传电影功能
@common.login_auth
def upload_movie_interface(back_dic):
    movie_size = back_dic.get('movie_size')
    movie_name = back_dic.get('movie_name')
    movie_new_name =  '文件大小{}Mb_'.format(round(movie_size/(1024*1024),3)) + movie_name

    movie_path = os.path.join(settings.DOWNLOAD_MOVIES_PATH, movie_new_name)

    # 2.存储电影信息于电影表中
    movie_obj = models.Movie(
        name=movie_new_name,
        is_free=back_dic.get('is_free'),
        is_delete=0,
        file_md5=back_dic.get('movie_md5'),
        path=movie_path,
        create_time=str(datetime.datetime.now()),
        user_id=back_dic.get('user_id')
    )
    movie_obj.save()


    send_dic = {
        'flag': True,
        'msg': '上传成功!',
        'movie_path': movie_path
    }

    return send_dic

@common.login_auth
def delete_movie_interface(back_dic, ):
    movie_id = back_dic.get('movie_id')
    movie_obj = models.Movie.select(models.Movie(),whereStr="id={0}".format(movie_id))[0]
    print(movie_obj.is_delete)
    movie_obj.is_delete = 1  # 0 --> 1
    movie_obj.update()

    send_dic = {
        'flag': True,
        'msg': '电影删除成功!'
    }

    return send_dic
    # common.send_msg(send_dic, conn)

#发送公告
@common.login_auth
def send_notice_interface(back_dic, ):

    notice_obj = models.Notice(
        title=back_dic.get('title'),
        content=back_dic.get('content'),
        create_time=str(datetime.datetime.now()),
        user_id=back_dic.get('user_id')
    )
    # 插入公告
    notice_obj.save()

    send_dic = {
        'msg': '公告发布成功!'
    }
    return send_dic
    # common.send_msg(send_dic, conn)

