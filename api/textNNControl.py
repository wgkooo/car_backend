"""
情感正负处理
"""
from fastapi import APIRouter, status
from textNN.deal_comment import *
from dao.koubei import *
from deal.textNN_deal import *
from models.textNN_models import *
from deal.koubei_deal import *

router = APIRouter(tags=["认证相关"], responses={404: {"description": "Not found"}})

@router.get("/emotion", summary="登陆")
async def user_login(text):
    result = predict_zfz(text)
    print(type(result))

    return {result}

"""
brand、name、comment、情感正负中、正个数、负个数、中个数
name和date查询这个东西的评论
"""
@router.get('/selectEmotionByBrandAndName', summary="")
async def selectEmotionByBrandAndName(name, date):
    # 如果date为空，则查询上月的数据
    if date == '':
        date = get_last_month_start()

    data = selectAllByNameAndDate_Dao(name, date)
    resultComment, listNegativeNum, listMiddleNum, listPositiveNum = selectEmotionByBrandAndName_deal(data)

    comment = ''
    for item in resultComment:
        comment += item + '\n'

    result = emotionModel()
    if len(data) > 0:
        result.brand = data[0][0]
        result.name = name
        result.comment = comment
        emotion = listNegativeNum + listMiddleNum + listPositiveNum
        if emotion > 0:
            result.emotion = 1
        if emotion == 0:
            result.emotion = 0
        if emotion < 0:
            result.emotion = -1
        result.negativeNums = listNegativeNum
        result.middleNums = listMiddleNum
        result.positiveNums = listPositiveNum

    return {'result': result}






