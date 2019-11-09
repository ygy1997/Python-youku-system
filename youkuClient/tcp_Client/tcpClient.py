import json
import struct
import socket
import threading

from conf import comm


class TcpClient:
    def __init__(self):
        self.tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.ip="127.0.0.1"
        self.port=9527
        self.tcp_client_start()

    def tcp_client_start(self):
        """
        功能函数，TCP客户端连接其他服务端的方法
        :return:
        """
        self.tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # self.tcp_socket.setblocking(False)
        try:
            self.address = (str(self.ip), int(self.port))
        except Exception as ret:
            self.msg = '请检查目标IP，目标端口\n'
            print(self.msg)
        else:
            try:
                self.msg = '正在连接目标服务器\n'
                print(self.msg)
                self.tcp_socket.connect(self.address)
            except Exception as ret:
                self.msg = '无法连接目标服务器\n'
                print(self.msg)
                print(ret)
            else:
                self.client_th = threading.Thread(target=self.tcp_client_concurrency)
                self.client_th.start()
                self.msg = 'TCP客户端已连接IP:%s端口:%s\n' % self.address
                print(self.msg)

    def tcp_client_concurrency(self):
        while True:
                try:
                    headers = self.tcp_socket.recv(4)
                    if headers:
                        data_len = struct.unpack('i', headers)[0]
                        json_data = self.tcp_socket.recv(data_len)
                        self.msg = '向服务器 接受了长度为{}字节的数据:\n\n'.format( data_len)
                        print(self.msg)
                        back_dic = json.loads(json_data.decode('utf-8'))
                        comm.back_dic = back_dic
                except Exception as e:
                    self.tcp_socket.close()
                    self.msg = '从服务器断开连接\n'
                    print(self.msg)
                    break


    def tcp_client_send(self,user_dic):
        json_data = json.dumps(user_dic).encode('utf-8')
        headers = struct.pack('i', len(json_data))
        self.tcp_socket.send(headers)
        self.tcp_socket.send(json_data)
        print(self.msg)
# user_dic = {
#     'username': '杨归元',
#     'password': '1054660480',
#     'user_type': 'admin',
#     'type': 'register'
# }
# tcpclient = TcpClient()
# register(tcpclient)





