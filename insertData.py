#!/usr/bin/env python
# coding: utf-8
##技术交流 QQ群：198447500
###说明：该代码仅限python学习研究使用，请谨慎复制粘贴直接使用,一定要懂哈。
import pymysql
import gevent
import time


class MyPyMysql:
    def __init__(self, host, port, username, password, db, charset='utf8'):
        self.host = host          # mysql主机地址
        self.port = port          # mysql端口
        self.username = username  # mysql远程连接用户名
        self.password = password  # mysql远程连接密码
        self.db = db              # mysql使用的数据库名
        self.charset = charset    # mysql使用的字符编码,默认为utf8
        self.pymysql_connect()    # __init__初始化之后，执行的函数

    def pymysql_connect(self):
        # pymysql连接mysql数据库
        # 需要的参数host,port,user,password,db,charset
        self.conn = pymysql.connect(host=self.host,
                                    port=self.port,
                                    user=self.username,
                                    password=self.password,
                                    db=self.db,
                                    charset=self.charset
                               )
        # 连接mysql后执行的函数
        self.asynchronous()

    def run(self, nmin, nmax):
        # 创建游标
        self.cur = self.conn.cursor()
        
        # 定义sql语句,插入数据id,name,gender,email
        sql = "insert into Persons(PersonID,Lastname,Firstname,Address,City) values (%s,%s,%s,%s,%s)"

        # 定义总插入行数为一个空列表
        data_list = []
        for i in range(nmin, nmax):
            # 添加所有任务到总的任务列表
            result = (1000+i, 'Mohan'+str(i), 'MAC'+str(i), 'TH'+str(i) , 'GZ'+str(i))
            data_list.append(result)
        #print (data_list)    
        # 执行多行插入，executemany(sql语句,数据(需一个元组类型))
        content = self.cur.executemany(sql, data_list)
        if content:
             print('成功插入第{}条数据'.format(nmax-1))
            
        # 提交数据,必须提交，不然数据不会保存
        self.conn.commit()


    def asynchronous(self):
        # g_l 任务列表
        # 定义了异步的函数: 这里用到了一个gevent.spawn方法
        max_line = 10000  # 定义每次最大插入行数(max_line=10000,即一次插入10000行)
        g_l = [gevent.spawn(self.run, i, i+max_line) for i in range(1, 100001, max_line)]

        # gevent.joinall 等待所以操作都执行完毕
        gevent.joinall(g_l)
        self.cur.close()  # 关闭游标
        self.conn.close()  # 关闭pymysql连接


if __name__ == '__main__':
    start_time = time.time()  # 计算程序开始时间
    st = MyPyMysql('127.0.0.1', 3306, 'root', 'password', 'LIN')  # 实例化类，传入必要参数
    print('程序耗时{:.2f}'.format(time.time() - start_time))  # 计算程序总耗时