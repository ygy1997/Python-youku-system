import time

import os

from conf import comm, settings
from tcp_Client.tcpClient import TcpClient
def download_pay_movie(client):
    if not comm.user_info.get('is_vip'):
        buy = input('普通用户购买视频原价20元一部,输入y确认购买:').strip()
    else:
        buy = input('VIP用户购买视频打骨折，10元一部,输入y确认购买:').strip()

    if not buy == 'y':
        print('取消购买')
        return

    while True:

        send_dic = {
            'type': 'get_movie_list',
            'movie_type': 'pay',
            'session':comm. user_info.get('cookies')
        }

        # 1.发送获取收费视频请求
        client.tcp_client_send(send_dic)
        i = 0
        while not comm.back_dic:
            i += 1
            if i % 7 == 0:
                print('连接失败')
                return
            print("\n正在等待服务器发送数据\n")
            time.sleep(1)

        if comm.back_dic.get('flag'):
            # 2.打印所有收费视频，让用户选择
            movie_list = comm.back_dic.get('movie_list')
            for index, movie_l in enumerate(movie_list):
                print(index, movie_l)

            choice = input('请输入下载电影的编号:').strip()
            if not choice.isdigit():
                print('请输入数字')
                continue

            choice = int(choice)

            if choice not in range(len(movie_list)):
                print('请输入正确编号!')
                continue

            # [电影的名字、免费、电影id]
            movie_name, is_free, movie_id = movie_list[choice]

            movie_path_client = os.path.join(
                settings.DOWNLOAD_MOVIE_PATH, movie_name
            )

            send_dic = {
                'type': 'download_movie',
                'movie_name': movie_name,
                'session': comm.user_info.get('cookies'),
                'movie_id': movie_id,
                'id':comm.user_info.get('id'),
                'is_vip': comm.user_info.get('is_vip')
            }

            comm.back_dic = None
            client.tcp_client_send(send_dic)
            i = 0
            while not comm.back_dic:
                i += 1
                if i % 7 == 0:
                    print('连接失败')
                    return
                print("\n正在等待服务器发送数据")
                time.sleep(1)

            if comm.back_dic.get('flag'):
                print('请等待广告')
                time.sleep(comm.back_dic.get('wait_time'))
                movie_path= comm.back_dic.get('movie_path')
                print('开始从{}下载...'.format(movie_path))
                with open(movie_path, 'rb') as f1:
                    with open(movie_path_client, 'wb') as f2:
                        data = f1.read()
                        f2.write(data)
                print('已经下载完成，{}'.format(movie_path_client))
                break

def download_free_movie(client):
    while True:
        comm.back_dic=None
        send_dic = {
            'type': 'get_movie_list',
            'movie_type': 'free',
            'session': comm.user_info.get('cookies')
        }
        client.tcp_client_send(send_dic)
        i = 0
        while not comm.back_dic:
            i += 1
            if i % 7 == 0:
                print('连接失败')
                return
            print("\n正在等待服务器发送数据\n")
            time.sleep(1)

        if comm.back_dic.get('flag'):
            movie_list = comm.back_dic.get('movie_list')
            for index,movie in enumerate(movie_list):
                print(index,movie)
            choice = input('请输入下载电影的编号：').strip()
            if choice == 'q':
                break
            if not choice.isdigit():
                print('请输入数字')
                continue
            choice=int(choice)

            movie_name, is_free, movie_id = movie_list[choice]

            # 电影存放目录
            movie_path_client = os.path.join(
                settings.DOWNLOAD_MOVIE_PATH, movie_name
            )

            send_dic = {
                'type': 'download_movie',
                'movie_name': movie_name,
                'session': comm.user_info.get('cookies'),
                'movie_id': movie_id,
                'id': comm.user_info.get('id'),
                'is_vip': comm.user_info.get('is_vip')
            }

            comm.back_dic = None
            client.tcp_client_send(send_dic)
            i = 0
            while not comm.back_dic:
                i += 1
                if i % 7 == 0:
                    print('连接失败')
                    return
                print("\n正在等待服务器发送数据")
                time.sleep(1)

            if comm.back_dic.get('flag'):
                print('请等待广告')
                time.sleep(comm.back_dic.get('wait_time'))
                movie_path= comm.back_dic.get('movie_path')
                print('开始从{}下载...'.format(movie_path))
                with open(movie_path, 'rb') as f1:
                    with open(movie_path_client, 'wb') as f2:
                        data = f1.read()
                        f2.write(data)
                print('已经下载完成，{}'.format(movie_path_client))
                break

def check_movies(client):
    send_dic = {
        'type': 'get_movie_list',
        'movie_type': 'all',
        'session': comm.user_info.get('cookies')
    }
    client.tcp_client_send(send_dic)
    i = 0
    while not comm.back_dic:
        i += 1
        if i % 7 == 0:
            print('连接失败')
            return
        print("\n正在等待服务器发送数据\n")
        time.sleep(1)

    if comm.back_dic.get('flag'):
        for movie in comm.back_dic.get('movie_list'):
            print(movie)

    else:
        print(comm.back_dic.get('msg'))

def buy_vip(client):

    if comm.user_info.get('is_vip'):
        print('已经是会员爸爸了!')
        return

    is_vip = input('请输入Y确认购买或者N取消: ').strip()
    if is_vip == 'y':

        send_dic = {
            'type': 'buy_vip',
            'username':comm.user_info.get('username'),
            'session': comm.user_info.get('cookies')
        }

        client.tcp_client_send(send_dic)
        i = 0
        while not comm.back_dic:
            i += 1
            if i % 7 == 0:
                print('连接失败')
                return
            print("\n正在等待服务器发送数据\n")
            time.sleep(1)

        print(comm.back_dic.get('msg'))

        comm.user_info['is_vip'] = 1
    else:
        print('取消购买!')

def check_download_record(client):
    send_dic = {
        'type': 'check_dowload_record',
        'id': comm.user_info.get('id'),
        'session': comm.user_info.get('cookies')
    }
    client.tcp_client_send(send_dic)
    i = 0
    while not comm.back_dic:
        i += 1
        if i % 7 == 0:
            print('连接失败')
            return
        print("\n正在等待服务器发送数据\n")
        time.sleep(1)

    if comm.back_dic.get('flag'):
        for movie_name, download_time in comm.back_dic.get('movie_list'):
            print(f'电影名称: {movie_name}')
            print(f'电影下载时间: {download_time}')
    else:print(comm.back_dic.get('msg'))

def check_notice(client):
    send_dic = {
        'type': 'check_notice',
        'session': comm.user_info.get('cookies')
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
        print(comm.back_dic.get('notice_list'))
    print(comm.back_dic.get('msg'))

func_dic = {
    '1': comm.register,
    '2': comm.login,
    '3': buy_vip,
    '4': check_movies,
    '5': download_free_movie,
    '6': download_pay_movie,
    '7':  check_download_record,
     '8': check_notice,
}

def user_view():
    client = TcpClient()

    while True:
        print('''
        1 注册
        2 登录
        3 冲会员
        4 查看视频
        5 下载免费视频
        6 下载收费视频
        7 查看下载记录
        8 查看公告
        ''')

        choice = input('请输入普通用户功能编号:').strip()

        if choice == 'q':
            break

        if choice not in func_dic:
            continue
        comm.back_dic = None
        func_dic.get(choice)(client)
