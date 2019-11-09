

from aiomysql.sa import create_engine

from sqlalchemy import Column, Integer, String, MetaData, Table, select, func



class DBcontroller:
    __engine=None
    __isinstance = False
    def __new__(cls, *args, **kwargs):
        if cls.__isinstance:  # 如果被实例化了
            return cls.__isinstance  # 返回实例化对象
        print('connecting to database...')
        cls.__isinstance = object.__new__(cls)  # 否则实例化
        return cls.__isinstance  # 返回实例化的对象

    @staticmethod
    async def connect():
        try:
            __engine = await create_engine(user='root',
                                              db='youku',
                                              host='127.0.0.1',
                                              password='root',
                                              minsize=1,
                                              maxsize=10,
                                              autocommit=True)
            if __engine:
                DBcontroller.__engine = __engine
                DBcontroller.connectStatue =True
                print('connect to mysql success!')
            else:
                raise ("connect to mysql error ")
        except:
            print('connect error.', exc_info=True)

    # def selectTable(self,sql):
    #     res=''
    #     async def select(res):
    #         conn = await DBcontroller.__engine.acquire()
    #         try:
    #             result = await conn.execute(sql)
    #             res = await result.fetchall()
    #             # for row in res:
    #             #     print(row)
    #         except Exception as e :
    #             print(e)
    #         finally:
    #             DBcontroller.__engine.release(conn)
    #             return res
    #     res = asyncio.get_event_loop().run_until_complete(select(res))
    #     return res

    async def select(self,sql):
        res=''
        conn = await DBcontroller.__engine.acquire()
        try:
            result = await conn.execute(sql)
            res = await result.fetchall()
            # for row in res:
            #     print(row)
        except Exception as e:
            print(e)
        finally:
            DBcontroller.__engine.release(conn)
            return res

    # res = asyncio.get_event_loop().run_until_complete(select(res))
    #
    # def executeTable(self,sql):
    #     res=''
    #     async def execute(res,sql):
    #         conn = await DBcontroller.__engine.acquire()
    #         try:
    #             result = await conn.execute(sql)
    #             res = result.lastrowid
    #             print('操作执行完毕')
    #         except Exception as e:
    #             if e.args[0]== 1062:
    #                 print('主键已存在')
    #             else:
    #                 print(f'插入失败:{e}')
    #         finally:
    #             DBcontroller.__engine.release(conn)
    #             return res
    #     lastrowid = asyncio.get_event_loop().run_until_complete(execute(res,sql))
    #     return lastrowid

    async def execute(self,sql):
        conn = await DBcontroller.__engine.acquire()
        res=''
        try:
            result = await conn.execute(sql)
            res = result.lastrowid
            print('操作执行完毕')
        except Exception as e:
            if e.args[0] == 1062:
                print('主键已存在')
            else:
                print(f'插入失败:{e}')
        finally:
            DBcontroller.__engine.release(conn)
            return res

    # def updateTable(self,table,id,attr):
    #     async def update():
    #         dbstb={
    #             'user':user
    #         }
    #         conn = await DBcontroller.__engine.acquire()
    #
    #         try:
    #             await conn.execute(user.update().where(dbstb[table].c.id==id).values(attr))
    #
    #         except Exception as e:
    #             if e.args[0]== 1062:
    #                 print('主键已存在')
    #             elif e.args[0]==1366:
    #                 if attr['id']=='':
    #                     print('未设置主键')
    #                 elif attr['is_vip']=='':
    #                     print('未设置vip类型')
    #                 elif attr['is_locked']=='':
    #                     print('未设置上锁类型')
    #                 else:print('未知错误，请联系管理员')
    #                 print(e)
    #             else:
    #                 print(f'connect failed:{e}')
    #         finally:
    #             DBcontroller.__engine.release(conn)
    #     asyncio.get_event_loop().run_until_complete(update())



