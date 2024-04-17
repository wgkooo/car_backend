"""
体验的数据
"""
from fastapi import APIRouter

router = APIRouter(tags=["体验的control"])

# 获取体验的数据
@router.get("/getdatas", summary='')
async def queryCarAllModel(brand: str):
    result = []
    if brand == 'SVW':
        result.append(3.62)
        result.append(3.62)
        result.append(3.62)
        result.append(3.61)
        result.append(3.59)
        result.append(3.59)
        result.append(3.59)
        result.append(3.59)

    if brand == 'Skoda':
        result.append(3.58)
        result.append(3.55)
        result.append(3.53)
        result.append(3.52)
        result.append(3.52)
        result.append(3.53)
        result.append(3.62)
        result.append(3.61)
    if brand == 'FAW-VW':
        result.append(3.56)
        result.append(3.54)
        result.append(3.52)
        result.append(3.52)
        result.append(3.48)
        result.append(3.44)
        result.append(3.46)
        result.append(3.44)
    print(result)
    return {'result': result}
