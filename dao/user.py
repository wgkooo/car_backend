import pymysql
from models.user import *

# 连接数据库
def getUser_Dao(user: userModel):
    conn = pymysql.connect(host='localhost', user='root', passwd='12345678', db='showcar', charset="utf8")
    cur = conn.cursor()

    # 查询数据库中，此关键词在微博中搜索到的新闻的最新时间
    sql = "select username, password from user where username=(%s) and password=(%s)"
    cur.execute(sql, (user.username, user.password))
    result = cur.fetchall()

    # 关闭数据库
    cur.close()
    conn.commit()
    conn.close()

    return result