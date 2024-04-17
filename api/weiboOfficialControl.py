"""
对微博的 official 进行操作
"""

from fastapi import APIRouter, status
from dao.weiboOfficial import *

router = APIRouter(tags=["操作汽车品牌官方微博的数据"])

@router.post('/getDate')
async def getDate():
    """
    :return: 查询目前为止100天的日期，不包括当天，从前一天开始
    """
    returnDate = query_100_days_datas()

    return returnDate

@router.post('/selectAllByTime')
async def selectAllByTime(dates=None): # dates=None 表示这个参数是可选参数，请求的时候可以不传入
    """
    :return: 返回这几个品牌中，一周内官方微博讨论的最多的三个帖子
    """
    dates = '2021-05-06'
    returnDate = searchAllByTime(dates)

    return returnDate

@router.post('/getOfficialWeiBo')
async def getOfficialWeiBo(brand: str, dates=None):
    """
    :param brand:
    :return: 返回某个品牌的 关注、粉丝、帖子数量、爬取时间
    """
    dates = '2021-05-06'
    returnDate = searchUserInfo(brand, dates)

    return returnDate

@router.post('/wordcloud')
async def wordcloud(brand: str, dates=None):
    """
    :param brand:
    :param dates:
    :return: 根据brand和dates，查询某一天的数据， 将这一天分词返回
    """
    dates = '2021-05-06'
    returnDate = searchWordCloudData(brand, dates)

    return returnDate
