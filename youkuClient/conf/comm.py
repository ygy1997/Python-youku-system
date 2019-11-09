import time

back_dic = None

user_info = {
    'cookies': None,
    'id':None,
    'is_vip':None
}

def register(client):
    global back_dic
    flag = False
    while not flag:
        back_dic = None
        usertype= 'admin' if input('''请输入登陆用户类型:
                                0：admin
                                其他：user \n''').strip()=='0' else 'user'
        username = input('请输入用户名:').strip()
        password = input('请输入密码:').strip()
        re_password = input('请确认密码:').strip()
        if password == re_password:
            user_dic = {
                'username': username,
                'password': password,
                'user_type': usertype,
                'type': 'register'
            }
            client.tcp_client_send(user_dic)
            i=0
            while not back_dic:
                i+=1
                print("\n正在等待服务器发送数据\n")
                time.sleep(1)
            print(back_dic)
            print(back_dic.get('msg'))
            flag = back_dic.get('flag')
        else:
            print('两密码不一致。')

def login(client):
    global back_dic
    flag = False
    while not flag:
        back_dic=None
        usertype= 'admin' if input('''请输入登陆用户类型:
                                0：admin
                                其他：user \n''').strip()=='0' else 'user'
        username = input('请输入用户名:').strip()
        password = input('请输入密码:').strip()
        print(usertype)
        send_dic = {
            'type': 'login',
            'username': username,
            'password': password,
            'user_type': usertype
        }
        client.tcp_client_send(send_dic)

        i = 0
        while not back_dic:
            i += 1
            if i%7==0:
                print('连接失败')
                return
            print("\n正在等待服务器发送数据\n")
            time.sleep(1)

        flag = back_dic.get('flag')
        if back_dic.get('flag'):
            user_info['is_vip'] = back_dic.get('is_vip')
            user_info['cookies'] = back_dic.get('session')
            user_info['id'] = back_dic.get('id')
        print(back_dic.get('msg'))