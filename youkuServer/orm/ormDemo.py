import asyncio

from sqlalchemy import select, text

from db.dbController import DBcontroller


class Model:
    loop =asyncio.get_event_loop()
    loop.run_until_complete(DBcontroller.connect())
    db = DBcontroller()
    def select(self,whereStr=None,lastId=None):
        #判断是不是更新过
        if lastId ==None:
            #不需要选择条件
            if whereStr==None:
                sqlStr=select('*').select_from(self.__table__)
            #搜索需要选择条件
            else:
                # print(self.id)

                sqlStr=select('*').select_from(self.__table__)\
                    .where(text(whereStr))
            print(sqlStr)
        #更新过了
        else:
            sqlStr = select('*').select_from(self.__table__) \
                .where(self.__table__.c.id == lastId)

        res = self.loop.run_until_complete(self.db.select(sql=sqlStr))

        #返回一个对象
        obj = type(self)#获取对象类型
        newobjList = []#新建对象列表
        for rows in res:
            newobj = obj()
            for key, value in rows.items():
                newobj.__dict__[key] = value
            newobjList.append(newobj)#新生成一个对象
        return newobjList

    #新增数据：需要对这个人是否存在
    def save(self, ):
        attr = self.__dict__.copy()
        attr.pop('_sa_instance_state')
        sqlStr= self.__table__.insert().values(attr)
        print(sqlStr)
        #获得插入数据的ID,并将属性值传给自己
        lastid = self.loop.run_until_complete(self.db.execute(sql=sqlStr))
        # lastid =self.db.executeTable(sql=sqlStr)
        res = self.select(lastId=lastid)
        return res


    # 修改:是基于已经存在了的数据进行修改操作
    def update(self,whereStr=None):
        if whereStr==None:
            whereStr = "id = {}".format(self.__dict__['id'])
        attr = self.__dict__.copy()
        attr.pop('_sa_instance_state')
        attr.pop('id')
        sqlStr = self.__table__.update().values(attr).where(text(whereStr))
        print(sqlStr)
        self.loop.run_until_complete(self.db.execute(sql=sqlStr))
        print('更新操作结束')

