import pymysql

conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='19961027', db='share_charge', charset='UTF8')
cur = conn.cursor()
name = 'SAM'
cur.execute("SELECT * FROM USER WHERE USER_NAME = '" + name + "'")
for i in cur:
    print(i)
cur.close()
conn.close()
