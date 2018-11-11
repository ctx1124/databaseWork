import pymysql

db = pymysql.connect("127.0.0.1","root","password","LIN")

cursor = db.cursor()
sql="CREATE TABLE test (age  int(20) ,money  int(20))"
cursor.execute(sql)

#data = cursor.fetchall()

#print(data)

db.close