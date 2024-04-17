"""
对微博的 huati 进行操作
"""

from fastapi import APIRouter
from dao.weiboHuati import *

router = APIRouter(tags=["操作汽车品牌话题的数据"])

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
    :return: 返回这几个品牌中，一周内话题评论最多的三个帖子
    """
    returnDate = searchAllByTime(dates)

    return returnDate

@router.post('/getHuatiInfo')
async def getHuatiInfo(topicname: str, dates=None):
    """
    :param brand:
    :return: 返回某个品牌的 关注、粉丝、帖子数量、爬取时间
    """
    returnDate = searchUserInfo(topicname, dates)

    return returnDate

@router.post('/wordcloud')
async def wordcloud(brand: str, dates=None):
    """
    :param brand:
    :param dates:
    :return: 根据brand和dates，查询某一天的数据， 将这一天分词返回
    """
    returnDate = searchWordCloudData(brand, dates)

    return returnDate