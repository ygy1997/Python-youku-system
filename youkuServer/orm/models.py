# coding: utf-8
from sqlalchemy import Column, Date, Enum, Float, String, Table, text, ForeignKey
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.ext.declarative import declarative_base
from orm.ormDemo import Model

Base = declarative_base()

class DownloadRecord(Base,Model):
    __tablename__ = 'download_record'

    id = Column(INTEGER(11), primary_key=True)
    user_id = Column(INTEGER(11),ForeignKey('user.id'))
    movie_id = Column(INTEGER(11))
    download_time= Column(String(255))

class Movie(Base,Model):
    __tablename__ = 'movie'

    id = Column(INTEGER(11), primary_key=True)
    name = Column(String(64))
    path = Column(String(255))
    is_free = Column(INTEGER(11), nullable=False, server_default=text("'1'"))
    is_delete = Column(INTEGER(11), nullable=False, server_default=text("'0'"))
    create_time = Column(String(255))
    file_md5 = Column(String(255))
    user_id = Column(INTEGER(11),ForeignKey('user.id'))


class Notice(Base,Model):
    __tablename__ = 'notice'

    id = Column(INTEGER(11), primary_key=True)
    title = Column(String(255))
    content = Column(String(255))
    user_id = Column(INTEGER(11),ForeignKey('user.id'))
    create_time = Column(String(255))


class User(Base,Model):
    __tablename__ = 'user'

    id = Column(INTEGER(11), primary_key=True)
    name = Column(String(255))
    password = Column(String(255))
    is_locked = Column(INTEGER(11), nullable=False, server_default=text("'0'"))
    is_vip = Column(INTEGER(11), nullable=False, server_default=text("'0'"))
    user_type = Column(String(255))
    register_time = Column(String(255))

# ygy = User()
# ygy.__dict__['id']=3
# print(ygy.id)
# all_user = User.select(User(name='杨归元'))
# for user in all_user:
#     print(user.__dict__)

# user = User.select(User(id=4))
# print(user.sort())
# attr = user[0].__dict__.copy()
# attr.pop('_sa_instance_state')
# # print(user[0].__dict__)
# user = User(name='杨归元',password='010101',register_time='2019/1')
# user = user.saveTB()
# user.password='123456'
# user.updateTB()
# print(user.__dict__)
# print(user.__dict__)
# print(user.is_vip)
# user.save()
# user[0].save()
# print(user[0].__repr__())
# print(user[0].__dict__)
# user[0].select暴露()
# UserList=[]
# for rows in attr:
#     user = User()
#     for key, value in rows.items():
#         user.__dict__[key] = value
#     UserList.append(user)
# print(UserList[0].__dict__)
# attr=(3, '杨归元', None, 0, 0, 'user', '2019/1')


