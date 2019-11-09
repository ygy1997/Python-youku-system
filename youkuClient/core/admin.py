import os
import time

from conf import settings, comm
from conf.comm import user_info
from lib import common
from tcp_Client.tcpClient import TcpClient

def upload_movie(client):
    flag = False
    while not flag:
        comm.back_dic = None
        # 1.打印所有电影名字
        if os.path.exists(settings.UPLOAD_MOVIE_PATH):
            movie_list = os.listdir(settings.UPLOAD_MOVIE_PATH)
            if not movie_list:
                print('没有可上传的电影')
                break

            for index, movie in enumerate(movie_list):
                print(index, movie)

            choice = input('请输入上传的电影编号:').strip()

            if choice=='q':
                break

            if not choice.isdigit():
                print('请输入数字')
                continue

            choice = int(choice)

            if choice not in range(len(movie_list)):
                print('请输入正确编号!')
                continue

            movie_name = movie_list[choice]


            # 上传电影的路径
            movie_path = os.path.join(settings.UPLOAD_MOVIE_PATH, movie_name)

            # 获取电影的md5值
            movie_md5 = common.get_movie_md5(movie_path)

            send_dic = {'type': 'check_movie',
                        'session': user_info.get('cookies'),
                        'movie_md5': movie_md5}

            client.tcp_client_send(send_dic)

            i = 0
            while not comm.back_dic:
                i += 1
                if i%7==0:
                    print('连接失败')
                    return
                print("\n正在等待服务器发送数据\n")
                time.sleep(1)
            print(comm.back_dic.get('msg'))

            if comm.back_dic.get('flag'):

                is_free = input('是否免费Y/N:').strip()

                free = 0
                if is_free == 'y':
                    free = 1

                send_dic = {
                    'type': 'upload_movie',
                    'session': comm.user_info.get('cookies'),
                    'movie_md5': movie_md5,
                    'movie_name': movie_name,
                    'is_free': free,
                    'movie_size': os.path.getsize(movie_path)
                }
                comm.back_dic = None

                # 开始上传电影
                client.tcp_client_send(
                    send_dic)
                i = 0

                while not comm.back_dic:
                                   i += 1
                if i%7==0:
                    print('连接失败')
                    return
                    print("\n正在等待服务器发送数据\n")
                    time.sleep(1)
                print("上传中...")

                movie_path_server = comm.back_dic.get('movie_path')
                with open(movie_path, 'rb') as f1:
                    with open(movie_path_server, 'wb') as f2:
                        data=f1.read()
                        f2.write(data)

                print(movie_path_server)
                flag = comm.back_dic.get('flag')



# 删除电影
def delete_movie(client):
    while True:
        comm.back_dic=None
        # 获取所有电影列表
        send_dic = {
            'type': 'get_movie_list',
            'session': user_info.get('cookies'),
            'movie_type':'all'
        }
        client.tcp_client_send(send_dic)
        i = 0
        while not comm.back_dic:
            i += 1
            if i%7==0:
                print('连接失败')
                return
            print("\n正在等待服务器发送数据\n")
            time.sleep(1)

        if comm.back_dic.get('flag'):
            back_movie_list = comm.back_dic.get('movie_list')
            # 打印所有未删除的电影
            for index, movie in enumerate(back_movie_list):
                print(index, movie)  # movie [电影的名字、是否免费、电影id]

            choice = input('请输入删除的电影编号:').strip()
            if choice=='q':
                break
            if not choice.isdigit():
                print('请输入数字')
                continue


            choice = int(choice)

            if choice not in range(len(back_movie_list)):
                print('请输入正确编号!')
                continue

            movie_list = back_movie_list[choice]

            movie_name, is_free, movie_id = movie_list

            print('什么电影正在删除...')

            send_dic = {
                'type': 'delete_movie',
                'session': user_info.get('cookies'),
                'movie_id': movie_id
            }

            comm.back_dic=None
            client.tcp_client_send(send_dic)
            i = 0
            while not comm.back_dic:
                i += 1
                if i%7==0:
                    print('连接失败')
                    return
                print("\n正在等待服务器发送数据\n")
                time.sleep(1)

            if comm.back_dic.get('flag'):
                print(comm.back_dic.get('msg'))
                break

        else:
            print('没有可删除的电影')
            break


# # 发布公告
def send_notice(client):
    title = input('请输入公告标题：').strip()
    content = input('请输入公告内容：').strip()

    send_dic = {
        'type': 'send_notice',
        'title': title,
        'content': content,
        'session': user_info.get('cookies')
    }

    client.tcp_client_send(send_dic)
    i = 0
    while not comm.back_dic:
        i += 1
        if i%7==0:
            print('连接失败')
            return
        print("\n正在等待服务器发送数据\n")
        time.sleep(1)
    print(comm.back_dic.get('msg'))

func_dic = {
    '1': comm.register,
    '2': comm.login,
    '3': upload_movie,
    '4': delete_movie,
    '5': send_notice,
}
def admin_view():
    client = TcpClient()
    while True:
        print('''
        1 注册
        2 登录
        3 上传视频
        4 删除视频
        5 发布公告
        ''')

        choice = input('请输入功能编号:').strip()
        if choice == 'q':
            break
        comm.back_dic = None
        if choice not in func_dic:
            continue
        func_dic.get(choice)(client)