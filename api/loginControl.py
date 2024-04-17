"""
登陆、注册功能
"""
from models.user import *
from fastapi import APIRouter, status
from starlette.requests import Request
from fastapi.responses import JSONResponse
from dao.user import *

router = APIRouter(tags=["认证相关"], responses={404: {"description": "Not found"}})

"""
async: 异步的关键字
登陆
"""
@router.post("/userLogin", summary="")
async def user_login(user: userModel):
    result = getUser_Dao(user)

    if len(result) == 0:
        # 返回错误的状态码
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # 返回正确的状态码
    return JSONResponse(status_code=status.HTTP_200_OK)