import pymysql
import arrow
import calendar
from models.discount import *

# 通过brand查询这个品牌12个月的打折数据
def query_12_months_datas(brand: str):
    returnData = []
    # 1. 获取目前为止12个月的日期
    current_date = arrow.now()
    for i in range(0, 12):
        last_month = current_date.shift(months=0-i).strftime("%Y-%m-%d")
        dis = RetunDataOfByBrand()
        dis.buyyear = last_month[0: 4]
        dis.buymonth = last_month[5: 7]
        dis.englishbuymonth = calendar.month_abbr[int(last_month[5:7])]
        dis.brand = brand[0: -1]
        dis.englishBrand = changeBrandToEnglish(brand[0: -1])
        returnData.append(dis)

    # 2. 按照月份查询打折数据
    # 2.1 连接数据库
    conn = pymysql.connect(host='localhost', user='root', passwd='12345678', db='showcar', charset="utf8")
    cur = conn.cursor()
    # 2.2 当月的数据未爬取，所以 discount = 0
    returnData[0].discount = '0.0'
    # 2.3 查询前11个月的数据
    for i in range(1, 12):
        # sql = "select brand, model, name from discount where brand = (%s) and "
        sql = 'select brand, carseries, luoche, zhidao, discount, buytime from discount WHERE brand like (%s) and buyyear=(%s) and buymonth=(%s)'
        cur.execute(sql, (brand, returnData[i].buyyear, returnData[i].buymonth))
        result = cur.fetchall()
        sum = 0.00
        for j in range(0, len(result)):
            sum += float(result[j][4])
        if sum == 0:
            returnData[i].discount = '0.0'
        else:
            returnData[i].discount = str(round(sum / len(result), 1))
    # 2.4
    #关闭数据库
    cur.close()
    conn.commit()
    conn.close()
    return returnData

def searchCarSeriesList(brand: str):
    carSeriesList = []
    # 连接数据库
    conn = pymysql.connect(host='localhost', user='root', passwd='12345678', db='showcar', charset="utf8")
    cur = conn.cursor()
    # 查询某个品牌的所有车型
    sql = "select distinct carseries from discount where brand like (%s)"
    brand = brand + '%'
    cur.execute(sql, (brand))
    result = cur.fetchall()
    for i in range(0, len(result)):
        carSeriesList.append(result[i][0])
    # 关闭数据库
    cur.close()
    conn.commit()
    conn.close()
    return carSeriesList

def query_12_months_datas_by_carseries(brand: str):
    " 1. 查询这个brand下的所有车系 "
    carSeriesList = searchCarSeriesList(brand)
    " 2. 连接数据库 "
    conn = pymysql.connect(host='localhost', user='root', passwd='12345678', db='showcar', charset="utf8")
    cur = conn.cursor()
    returnlist = []
    for i in range(0, len(carSeriesList)):
        " 3. 获取某个车型12个月的车型数据 "
        returnData = []
        " 3.1 获取过去12个月的日期 "
        current_date =  arrow.now()
        for j in range(0, 12):
            last_month = current_date.shift(months=0-j).strftime("%Y-%m-%d")
            dis = RetunDataOfByBrand()
            dis.buyyear = last_month[0: 4]
            dis.buymonth = last_month[5: 7]
            dis.englishbuymonth = calendar.month_abbr[int(last_month[5:7])]
            dis.carseries = carSeriesList[i]
            returnData.append(dis)
        " 3.2 按照月份查询打折数据 "
        returnData[0].discount = '0.0' # 当月的数据未爬取，所以 discount = 0
        for j in range(1, 12):
            sql = "select carseries, luoche, zhidao, discount from discount where carseries=(%s) and buyyear=(%s) and buymonth=(%s)"
            cur.execute(sql, (carSeriesList[i], returnData[j].buyyear, returnData[j].buymonth))
            result = cur.fetchall()
            sum = 0.00
            for k in range(0, len(result)):
                sum += float(result[k][3])
            if sum == 0:
                returnData[j].discount = '0.0'
            else:
                returnData[j].discount = str(round(sum / len(result), 1))
        returnlist.append(returnData)

    # 关闭数据库
    cur.close()
    conn.commit()
    conn.close()
    return returnlist

def changeBrandToEnglish(brand):
    brands = {
        '奔驰': 'Mercedes-Benz',
        '宝马': 'BMW',
        '奥迪': 'Audi',
        '凯迪拉克': 'Cadillac',
        '路虎': 'Land Rover',
        '上汽大众': 'SAIC Volkswagen',
        '一汽大众': 'FAW-Volkswagen',
        '蔚来': 'NIO',
        '威马': 'Weltmeister',
        '小鹏': 'Xpeng',
        '理想': 'Li Auto',
        '比亚迪': 'BYD',
        '特斯拉': 'Tesla'
    }
    return brands.get(brand)

if __name__ == '__main__':
    result = query_12_months_datas_by_carseries('奔驰')
    print(result)
    print(len(result))
    print('------')
    for i in range(0, len(result)):
        print(len(result[i]))
        print(result[i][0].carseries)
