import uvicorn
from api import loginControl, koubeiControl, dealerTiYanControl, excelControl, textNNControl, \
    pieDatasControl, discountControl, weiboOfficialControl, weiboHuatiControl
from fastapi import FastAPI

app = FastAPI()

app.include_router(loginControl.router, prefix='/api/user')
app.include_router(koubeiControl.router, prefix='/api/koubei')
app.include_router(dealerTiYanControl.router, prefix='/api/dealertiyan')
app.include_router(excelControl.router, prefix='/api/easyExcel')
app.include_router(textNNControl.router, prefix='/api/textNNControl')
app.include_router(pieDatasControl.router, prefix="/api/piedatas")
app.include_router(discountControl.router, prefix='/api/discount')
app.include_router(weiboOfficialControl.router, prefix='/api/officialPost')
app.include_router(weiboHuatiControl.router, prefix='/api/huatiPost')






# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=8087)
