import os
import sys

from tcp_server.tcpServer import TcpServer

sys.path.append(
    os.path.dirname(__file__)
)


# 服务端入口
if __name__ == '__main__':
    server = TcpServer()
