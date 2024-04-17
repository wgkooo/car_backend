"""
对 discount 进行操作
"""
import json
import random

from fastapi import APIRouter, status
from starlette.requests import Request
from fastapi.responses import JSONResponse

from dao.discount import *



router = APIRouter(tags=["操作打折数据"])

# 查询参数是汽车的品牌，返回这个品牌12个月的打折信息
@router.post('/selectByBrandYearMonth', summary="")
async def selectByBrandYearMonth(brand: str):
    """
    :param brand:
    :return: 这个品牌12个月的打折数据
    """
    """
    1. 
    查询参数brand加一个 % 的原因是：数据库中brand字段存储的数据为
    奥迪A4L、奥迪A6L等形式，当查询参数为 奥迪 时，加一个%变成 奥迪%
    然后模糊查询所有brand字段中含有 奥迪 当数据
    """
    brand = brand + '%'
    print(brand)

    " 2. 返回到目前为止12个月的日期 "
    retunDataOfByBrands = query_12_months_datas(brand)


    return {'result': retunDataOfByBrands}


# 根据汽车品牌，返回这个品牌所有车系过去12个月的打折数据
@router.post("/selectAllCarseriesByBrand", summary="")
async def selectAllCarseriesByBrand(brand: str):
    """
    :param brand:
    :return: 这个品牌所有车系的12个月的打折数据
    """
    " 1. 将这个brand的英文转换为对应的中文 "
    brand = changeBrand(brand)
    " 2. 查询某个品牌下每个车型的数据，并且返回 "
    returnlist = query_12_months_datas_by_carseries(brand)

    return returnlist

def changeBrand(brand: str):
    brands = {
        'Mercedes-Benz': '奔驰',
        'BMW': '宝马',
        'Audi': '奥迪',
        'Cadillac': '凯迪拉克',
        'Land Rover': '路虎',
        'SAIC Volkswagen': '上汽大众',
        'FAW-Volkswagen': '一汽大众',
        'NIO': '蔚来',
        'Weltmeister': '威马',
        'Xpeng': '小鹏',
        'Li Auto': '理想',
        'BYD': '比亚迪',
        'Tesla': '特斯拉',
    }
    return brands.get(brand)