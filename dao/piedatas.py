import pymysql

def queryAllcategoryByBrand_Dao(brand):
    conn = pymysql.connect(host='localhost', user='root', passwd='12345678', db='showcar', charset="utf8")
    cur = conn.cursor()

    # 查询数据库
    sql = "select s.id, s.brand, s.category, s.categoryrate, s.commenttype " \
          "from (select *, row_number() over (partition by category) as group_idx " \
          "from piedatas where brand like (%s)) s " \
          "where s.group_idx = 1 GROUP BY id "
    cur.execute(sql, (brand))
    result = cur.fetchall()
    # 关闭数据库
    cur.close()
    conn.commit()
    conn.close()

    return result

if __name__ == '__main__':
    result = queryAllcategoryByBrand_Dao("BMW")
    print(result)