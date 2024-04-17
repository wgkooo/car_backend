from fastapi import APIRouter, status
from dao.koubei import *
from deal.koubei_deal import returnKoubeiExcel
from models.koubei import *
from openpyxl import Workbook
from fastapi.responses import StreamingResponse
from io import BytesIO
import xlsxwriter

router = APIRouter(tags=["操作导出excel表格"])

# 查询有哪些汽车品牌
@router.get("/queryAllBrand", summary='')
async def queryAllBrand():
    data = queryAllBrand_Dao()
    result = []
    for item in data:
        koubei = koubeiReturnModel()
        koubei.brand = item[0]
        result.append(koubei)

    return {'result': result}

# 根据brand查询这个品牌有哪些车型
@router.get("/queryAllNameByBrand", summary="")
async def queryAllNameByBrand(brand):
    data = queryAllNameByBrand_Dao(brand)
    result = []
    for item in data:
        koubei = koubeiReturnModel()
        koubei.name = item[0]
        result.append(koubei)

    return {'result': result}

# 分页查询
@router.get("/queryByKoubeiLimitQuery", summary="")
async def queryByKoubeiLimitQuery(brand, name, beginDate, endDate, pagenumber, contentnum):
    data = queryByKoubeiLimitQuery_Dao(brand, name, beginDate, endDate, pagenumber, contentnum)
    result = []
    for item in data:
        koubei = koubeiReturnModel()
        koubei.brand = item[1]
        koubei.name = item[2]
        koubei.model = item[3]
        koubei.carseries = item[4]
        koubei.overall = item[5]
        koubei.exterior = item[6]
        koubei.interior = item[7]
        koubei.carspace = item[8]
        koubei.valueformoney = item[9]
        koubei.power = item[10]
        koubei.maneuverability = item[11]
        koubei.fuelconsumption = item[12]
        koubei.comfort = item[13]
        koubei.optionsandfeatures = item[14]
        koubei.createdate = item[15]
        koubei.source = item[16]
        koubei.comment = item[17]
        result.append(koubei)

    return {'result': result}

# 查询分页查询的总条数
@router.get('/queryByKoubeiLimitAllNum', summary="")
async def queryByKoubeiLimitAllNum(brand, name, beginDate, endDate, pagenumber: int, contentnum: int):
    data = queryByKoubeiLimitAllNum_Dao(brand, name, beginDate, endDate)
    nums = int(len(data) / contentnum)
    if len(data) % contentnum > 0:
        nums += 1

    return {'result': nums}

# 在easyExcel，根据brand，name，beginDate，endDate将查询到的数据导出到excel
@router.get('/exportExcel', summary="")
async def exportExcel(brand, name, beginDate, endDate):
    data = queryByKoubeiLimitAllNum_Dao(brand, name, beginDate, endDate)
    output, headers = returnKoubeiExcel(data)
    return StreamingResponse(output, headers=headers)

# 在productEvaluationByCarModel页面，根据name将查询到的结果导出到excel
@router.get('/queryByKoubeiExcelSaveOneMonthDataQuery', summary="")
async def queryByKoubeiExcelSaveOneMonthDataQuery(name, date):
    data = queryByKoubeiExcelSaveOneMonthDataQuery_Dao(name, date)
    output, headers = returnKoubeiExcel(data)
    return StreamingResponse(output, headers=headers)




