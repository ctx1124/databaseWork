import pymysql

db = pymysql.connect("127.0.0.1","root","password","LIN")

cursor = db.cursor()
cursor.execute("SELECT VERSION()")

data = cursor.fetchall()

print(data)

db.close