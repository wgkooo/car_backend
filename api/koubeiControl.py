"""
对koubei进行操作
"""
import json
import random

from fastapi import APIRouter, status
from starlette.requests import Request
from fastapi.responses import JSONResponse

from dao.user import *
from dao.koubei import *

from deal.koubei_deal import *




router = APIRouter(tags=["操作口碑数据"])

# 通过brand查询所有的model
@router.get("/queryCarAllModel", summary='')
async def queryCarAllModel(brand: str):
    data = queryCarAllModel_Dao(brand)
    # 将元组数据转化为对象返回
    result = []
    for item in data:
        koubei = koubeiModel()
        koubei.brand = item[0]
        koubei.model = item[1]
        koubei.name = item[2]
        result.append(koubei)

    return {'result': result}

# 通过name自动选择对比车型的的name
@router.get("/autoSelectByModel", summary="")
async def autoSelectByModel(name: str):
    data = queryAllModel_Dao()
    brand = queryBrandByName_Dao(name)
    # 将元组数据转化为对象
    lists = []
    for item in data:
        if item[0] == brand:
            continue
        koubei = koubeiModel()
        koubei.brand = item[0]
        koubei.model = item[1]
        koubei.name = item[2]
        lists.append(koubei)
    result = []
    result.append(lists[random.randint(0, len(lists))])
    result.append(lists[random.randint(0, len(lists))])
    result.append(lists[random.randint(0, len(lists))])
    return {'result': result}

# 通过brand自动选择对比的车型
@router.get('/autoSelectByBrand', summary="")
async def autoSelectByBrand(brand: str):
    data = queryBrandByBrand_Dao(brand)
    lists = []
    for item in data:
        koubei = koubeiModel()
        koubei.brand = item[0]
        lists.append(koubei)

    result = []
    result.append(lists[random.randint(0, len(lists))])
    result.append(lists[random.randint(0, len(lists))])
    result.append(lists[random.randint(0, len(lists))])

    return {'result': result}

@router.get('/querydate', summary="")
async def querydate():
    "获取2020-09到上个月的如期数据"
    dataSet = get_DataSet()

    return {'dataSet': dataSet}

# 根据 name 和 date, 返回查询到的数据
@router.post('/selectAllByName', summary="")
async def selectAllByName(name: str, date: str):
    # 如果date为空，则查询上月的数据
    if date == '':
        date = get_last_month_start()
    data = selectAllByNameAndDate_Dao(name, str(date))

    # 将元组数据转化为对象
    result = changeKoubeiData(data)

    return {'result': result}

# 根据 brand 和 date，返回查询到的数据
@router.post('/selectAllByBrand', summary="")
async def selectAllByBrand(brand: str, date: str):
    # 如果date为空，则查询上个月的数据
    if date == '':
        date = get_last_month_start()
    data = selectAllByBrandAndDate_Dao(brand, str(date))

    # 将元祖数据转化为对象
    result = changeKoubeiData(data)

    return {'result': result}

"""
brand、name、comment、情感正负中、正个数、负个数、中个数
name和date查询这个东西的评论
"""
@router.get('/selectEmotionByBrandAndName', summary="")
async def selectEmotionByBrandAndName(name, date):
    " 根据name和date查询这个车型的 overall、exterior、interior等评论的正负性 "
    " 因为评论格式的原因，这里暂时先后去overall的数据 "
    if date == '':
        date = get_last_month_start()
    data = selectCommentByBrandAndDate_Dao(name, str(date))
    commentPer = deal_comment_percent(data)


    return {'result': commentPer}








