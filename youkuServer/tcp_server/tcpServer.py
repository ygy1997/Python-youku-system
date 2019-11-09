import json
import socket
import struct
import threading
import time

from interface import common_interface, admin_interface, user_interface

func_dic = {
    'register': common_interface.register_interface,
    'login': common_interface.login_interface,
    #
    # # 查看电影接口
    'check_movie': common_interface.check_movie_interface,
    'upload_movie': admin_interface.upload_movie_interface,
    #
    # # 获取电影列表接口
    'get_movie_list': common_interface.get_movie_list_interface,
    'delete_movie': admin_interface.delete_movie_interface,
    #
    # # 发布公告接口
    'send_notice': admin_interface.send_notice_interface,
    #
    'buy_vip': user_interface.buy_vip_interface,
    #
    # # 下载电影接口
    'download_movie': user_interface.download_movie_interface,
    'check_dowload_record': user_interface.check_dowload_record_interface,

    'check_notice': user_interface.check_notice_interface,

}

class TcpServer:
    def __init__(self):
        self.tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.client_socket_list = list()
        self.port = 9527
        self.tcp_server_start()

    def tcp_server_start(self):
        """
        功能函数，TCP服务端开启的方法
        :return: None
        """
        self.tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.tcp_socket.setblocking(False)
        try:

            self.tcp_socket.bind(('', self.port))
        except Exception as ret:
            self.msg = '请检查端口号\n'
            print(self.msg)
            print(ret)
        else:
            self.tcp_socket.listen()
            self.sever_th = threading.Thread(target=self.tcp_server_concurrency)
            self.sever_th.start()
            self.msg = 'TCP服务端正在监听端口:%s\n' % str(self.port)
            print(self.msg)


    def tcp_server_concurrency(self):
        """
        功能函数，供创建线程的方法；
        使用子线程用于监听并创建连接，使主线程可以继续运行，以免无响应
        使用非阻塞式并发用于接收客户端消息，减少系统资源浪费，使软件轻量化
        :return:None
        """
        while True:
            try:
                self.client_socket, self.client_address = self.tcp_socket.accept()

            except Exception as ret:
                time.sleep(0.001)

            else:
                self.client_socket.setblocking(False)
                # 将创建的客户端套接字存入列表
                self.client_socket_list.append((self.client_socket, self.client_address))
                self.msg = 'TCP服务端已连接IP:%s端口:%s\n' % self.client_address
                print(self.msg)
            # 轮询客户端套接字列表，接收数据
            for client, address in self.client_socket_list:
                try:
                    headers = client.recv(4)
                    data_len = struct.unpack('i', headers)[0]
                    json_data = client.recv(data_len)

                    # back_dic客户端传过来的字典数据
                    back_dic = json.loads(json_data.decode('utf-8'))
                    back_dic['addr'] = str( address[0])

                except Exception as ret:
                    pass
                else:
                    if headers:
                        self.msg = '来自IP:{}的端口:{}:\n发送了长度为{}字节的数据\n'.format(address[0], address[1],struct.unpack('i', headers)[0])
                        print(self.msg)
                        self.dispatcher(back_dic,client,address)
                    else:
                        client.close()
                        self.client_socket_list.remove((client, address))


    def tcp_server_send(self,send_dic,client,address,file=None):
        json_data = json.dumps(send_dic).encode('utf-8')

        headers = struct.pack('i', len(json_data))
        client.send(headers)
        client.send(json_data)
        if file:
            with open(file, 'rb') as f:
                for line in f:
                    client.send(line)
        self.msg = '服务器向IP:{}端口:{}:\n发送了长度为{}字节的数据\n'.format(address[0], address[1],struct.unpack('i', headers)[0])
        print(self.msg)

    # 做任务分发的工作
    def dispatcher(self,back_dic,client,address):

        type = back_dic.get('type')

        if type in func_dic:

            send_dic = func_dic.get(type)(back_dic)


        else:
            send_dic = {
                'flag': False,
                'msg': '请求错误!'
            }
        self.tcp_server_send(send_dic,client,address)



