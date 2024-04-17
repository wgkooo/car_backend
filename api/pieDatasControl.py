"""
饼图数据
"""
from fastapi import APIRouter, status
from dao.piedatas import *
from models.piedatas import *

router = APIRouter(tags=["认证相关"], responses={404: {"description": "Not found"}})

# 查询某个品牌的饼图数据
@router.post("/queryAllcategoryByBrand", summary="")
async def user_login(brand):
    data = queryAllcategoryByBrand_Dao(brand)

    # 将元组转化为对象
    "select s.id, s.brand, s.category, s.categoryrate, s.commenttype "
    result = []
    for item in data:
        piedata = piedatas()
        piedata.id = item[0]
        piedata.brand = item[1]
        piedata.category = item[2]
        piedata.categoryrate = item[3]
        piedata.commenttype = item[4]
        result.append(piedata)

    return {'result': result}
