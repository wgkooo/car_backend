import pymysql
from models.koubei import *
import pandas as pd


# 通过brand查询这个brand的所有车型的brand、model、name
def queryCarAllModel_Dao(brand: str):
    conn = pymysql.connect(host='localhost', user='root', passwd='12345678', db='showcar', charset="utf8")
    cur = conn.cursor()

    # 查询数据库
    sql = "select brand, model, name from koubei where brand = (%s) group by brand,model,name"
    cur.execute(sql, (brand))
    result = cur.fetchall()
    # 关闭数据库
    cur.close()
    conn.commit()
    conn.close()

    return result

# 查询所有车型的brand、model、name
def queryAllModel_Dao():
    conn = pymysql.connect(host='localhost', user='root', passwd='12345678', db='showcar', charset="utf8")
    cur = conn.cursor()

    # 查询数据库
    sql = "select brand, model, name from koubei group by brand,model,name"
    cur.execute(sql)
    result = cur.fetchall()
    # 关闭数据库
    cur.close()
    conn.commit()
    conn.close()

    return result

# 通过name查询brand
def queryBrandByName_Dao(name: str):
    conn = pymysql.connect(host='localhost', user='root', passwd='12345678', db='showcar', charset="utf8")
    cur = conn.cursor()

    # 查询数据库
    sql = "select brand from koubei where name=(%s) group by brand"
    cur.execute(sql, (name))
    result = cur.fetchall()
    # 关闭数据库
    cur.close()
    conn.commit()
    conn.close()

    return result

# 通过brand查询不包括这个brand的所有车型
def queryBrandByBrand_Dao(brand: str):
    conn = pymysql.connect(host='localhost', user='root', passwd='12345678', db='showcar', charset="utf8")
    cur = conn.cursor()

    # 查询数据库
    sql = "select brand from koubei where brand!=(%s) group by brand"
    cur.execute(sql, (brand))
    result = cur.fetchall()
    # 关闭数据库
    cur.close()
    conn.commit()
    conn.close()
    return result

# 通过 name 和 date 查询数据
def selectAllByNameAndDate_Dao(name:str, date:str):
    conn = pymysql.connect(host='localhost', user='root', passwd='12345678', db='showcar', charset="utf8")
    cur = conn.cursor()

    # 查询数据库
    sql = "select brand, model, name, carspace, comfort, exterior, fuelconsumption, interior, maneuverability, " \
          "optionsandfeatures, overall, power, valueformoney, createdate, comment from koubei where name = (%s) " \
          "and YEAR(createdate)=left((%s) ,4) and month(createdate)=substr((%s) ,6,7)"
    cur.execute(sql, (name, date, date))
    result = cur.fetchall()
    # 关闭数据库
    cur.close()
    conn.commit()
    conn.close()
    return result

# 通过 brand 和 date 查询数据
def selectAllByBrandAndDate_Dao(brand: str, date: str):
    conn = pymysql.connect(host='localhost', user='root', passwd='12345678', db='showcar', charset="utf8")
    cur = conn.cursor()

    # 查询数据库
    sql = "select brand, model, name, carspace, comfort, exterior, fuelconsumption, interior, maneuverability, " \
          "optionsandfeatures, overall, power, valueformoney, createdate from koubei where brand = (%s) " \
          "and YEAR(createdate)=left((%s) ,4) and month(createdate)=substr((%s) ,6,7)"
    cur.execute(sql, (brand, date, date))
    result = cur.fetchall()
    # 关闭数据库
    cur.close()
    conn.commit()
    conn.close()
    return result

# 通过brand 和 date 查询评论
def selectCommentByBrandAndDate_Dao(name: str, date: str):
    conn = pymysql.connect(host='localhost', user='root', passwd='12345678', db='showcar', charset="utf8")
    cur = conn.cursor()

    # 查询数据库
    sql = "select overallComment,exteriorComment,interiorComment,carspaceComment,valueformoneyComment,powerComment,maneuverabilityComment," \
          "fuelConsumptionComment,comfortCommennt,optionsandfeaturesComment from koubei where name = (%s) " \
          "and YEAR(createdate)=left((%s) ,4) and month(createdate)=substr((%s) ,6,7)"
    cur.execute(sql, (name, date, date))
    result = cur.fetchall()
    # 关闭数据库
    cur.close()
    conn.commit()
    conn.close()
    return result


# 查询总共有多少汽车的品牌
def queryAllBrand_Dao():
    conn = pymysql.connect(host='localhost', user='root', passwd='12345678', db='showcar', charset="utf8")
    cur = conn.cursor()

    # 查询数据库
    sql = "select distinct brand from koubei"
    cur.execute(sql)
    result = cur.fetchall()
    # 关闭数据库
    cur.close()
    conn.commit()
    conn.close()
    return result

# 查询这个品牌有多少个车型
def queryAllNameByBrand_Dao(brand: str):
    conn = pymysql.connect(host='localhost', user='root', passwd='12345678', db='showcar', charset="utf8")
    cur = conn.cursor()

    # 查询数据库
    sql = "select distinct name from koubei where brand = (%s)"
    cur.execute(sql, (brand))
    result = cur.fetchall()
    # 关闭数据库
    cur.close()
    conn.commit()
    conn.close()
    return result

# 分页查询
def queryByKoubeiLimitQuery_Dao(brand, name, beginDate, endDate, pagenumber, contentnum):
    conn = pymysql.connect(host='localhost', user='root', passwd='12345678', db='showcar', charset="utf8")
    cur = conn.cursor()

    # 查询数据库
    sql = "select id, brand, name, model, carseries, overall, exterior, interior, carspace, valueformoney, " \
          "power, maneuverability, fuelConsumption, comfort, optionsandfeatures, createdate, source, comment " \
          "from koubei where brand = (%s) and name = (%s) " \
          "and createdate > (%s) and createdate < (%s) limit %s, %s"
    cur.execute(sql, (brand, name, beginDate, endDate, int(pagenumber), int(contentnum)))
    result = cur.fetchall()
    # 关闭数据库
    cur.close()
    conn.commit()
    conn.close()
    return result

# 分页查询的总条数
def queryByKoubeiLimitAllNum_Dao(brand, name, beginDate, endDate):
    conn = pymysql.connect(host='localhost', user='root', passwd='12345678', db='showcar', charset="utf8")
    cur = conn.cursor()

    # 查询数据库
    sql = "select id, brand, name,carseries, model, overall, exterior, interior, carspace, valueformoney, " \
          "power, maneuverability, fuelConsumption, comfort, optionsandfeatures, createdate, source, comment " \
          "from koubei where brand = (%s) and name = (%s) " \
          "and createdate > (%s) and createdate < (%s)"
    cur.execute(sql, (brand, name, beginDate, endDate))
    result = cur.fetchall()
    # 关闭数据库
    cur.close()
    conn.commit()
    conn.close()
    return result

def queryByKoubeiExcelSaveOneMonthDataQuery_Dao(name, date):
    conn = pymysql.connect(host='localhost', user='root', passwd='12345678', db='showcar', charset="utf8")
    cur = conn.cursor()

    # 查询数据库
    sql = "select id, brand, name,carseries, model, overall, exterior, interior, carspace, valueformoney, " \
          "power, maneuverability, fuelConsumption, comfort, optionsandfeatures, createdate, source, comment " \
          "from koubei where name = (%s) and YEAR(createdate)=left((%s) ,4) and month(createdate)=substr((%s) ,6,7)"
    cur.execute(sql, (name, date, date))
    result = cur.fetchall()
    # 关闭数据库
    cur.close()
    conn.commit()
    conn.close()
    return result


if __name__ == '__main__':
    name = 'A4L'
    date = '2022-07-01'
    data = selectCommentByBrandAndDate_Dao(name, date)

