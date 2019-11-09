from core import user, admin

func_dic = {
    '1': admin.admin_view,
    '2': user.user_view,
}
def run():
    print('启动客户端...')
    while True:
        print('''
        请选择角色编号: 
            1 管理员
            2 普通用户
            q 退出
        ''')

        choice = input('请输入功能编号: ').strip()

        if choice == 'q':
            break

        if choice not in func_dic:
            continue

        func_dic.get(choice)()