from fastapi.responses import StreamingResponse
from io import BytesIO
import xlsxwriter
from datetime import datetime
from models.koubei import *
from textNN.deal_comment import *


def get_last_month_start(month_str=None):
    # 获取上一个月的第一天
    '''
    param: month_str 月份，2021-04
    '''
    # return: 格式 %Y-%m-%d
    if not month_str:
        month_str = datetime.now().strftime('%Y-%m')
    year, month = int(month_str.split('-')[0]), int(month_str.split('-')[1])
    if month == 1:
        year -= 1
        month = 12
    else:
        month -= 1
    month = '%02d' % month
    return '{}-{}-01'.format(year, month)

def get_next_month_start(month_str=None):
    # 获取下一个月的第一天
    '''
    param: month_str 月份，2021-04
    '''
    # return: 格式 %Y-%m-%d
    if not month_str:
        month_str = datetime.now().strftime('%Y-%m')
    year, month = int(month_str.split('-')[0]), int(month_str.split('-')[1])
    if month == 12:
        year += 1
        month = 1
    else:
        month += 1
    month = '%02d' % month
    return '{}-{}-01'.format(year, month)

# 获取指定时间段的日期
def get_DataSet():
    dateSet = []

    beginData = get_next_month_start('2020-07-01')
    endData = get_last_month_start() # 上个月1号

    while True:
        beginData = get_next_month_start(beginData)
        dateSet.append(beginData)
        if beginData == endData:
            break

    return dateSet

# 将元组数据转化为对象
def changeKoubeiData(data):
    if len(data) == 0:
        return koubeiReturnModel()

    koubei = koubeiReturnModel()
    carspaceNum = 0
    comfortNum = 0
    exteriorNum = 0
    fuelconsumptionNum = 0
    interiorNum = 0
    maneuverabilityNum = 0
    optionsandfeaturesNum = 0
    overallNum = 0
    powerNum = 0
    valueformoneyNum = 0
    # 计算总值
    for item in data:
        if item[3] != None:
            koubei.carspace += float(item[3])
            carspaceNum += 1
        if item[4] != None:
            koubei.comfort += float(item[4])
            comfortNum += 1
        if item[5] != None:
            koubei.exterior += float(item[5])
            exteriorNum += 1
        if item[6] != None:
            koubei.fuelconsumption += float(item[6])
            fuelconsumptionNum += 1
        if item[7] != None:
            koubei.interior += float(item[7])
            interiorNum += 1
        if item[8] != None:
            koubei.maneuverability += float(item[8])
            maneuverabilityNum += 1
        if item[9] != None:
            koubei.optionsandfeatures += float(item[9])
            optionsandfeaturesNum += 1
        if item[10] != None:
            koubei.overall += float(item[10])
            overallNum += 1
        if item[11] != None:
            koubei.power += float(item[11])
            powerNum += 1
        if item[12] != None:
            koubei.valueformoney += float(item[12])
            valueformoneyNum += 1

    # 计算平均值 并 找出strengths和weaknesses
    koubei.brand = data[0][0]
    koubei.model = data[0][1]
    koubei.name = data[0][2]
    strengths = ''
    strengthsValue = 0
    weaknesses = ''
    weaknessesValue = 0
    if carspaceNum > 0:
        koubei.carspace = format(koubei.carspace / carspaceNum, '0.2f')
        strengths = 'Car Space'
        strengthsValue = koubei.carspace
        weaknesses = 'Car Space'
        weaknessesValue = koubei.carspace
    else:
        koubei.carspace = 0

    if comfortNum > 0:
        koubei.comfort = format(koubei.comfort / comfortNum, '0.2f')
        if koubei.comfort > strengthsValue:
            strengthsValue = koubei.comfort
            strengths = 'Comfort'
        if koubei.comfort < weaknessesValue:
            weaknessesValue = koubei.comfort
            weaknesses = 'Comfort'
    else:
        koubei.comfort = 0

    if exteriorNum > 0:
        koubei.exterior = format(koubei.exterior / exteriorNum, '0.2f')
        if koubei.exterior > strengthsValue:
            strengthsValue = koubei.exterior
            strengths = 'Exterior'
        if koubei.exterior < weaknessesValue:
            weaknessesValue = koubei.exterior
            weaknesses = 'Exterior'
    else:
        koubei.exterior = 0

    if fuelconsumptionNum > 0:
        koubei.fuelconsumption = format(koubei.fuelconsumption / fuelconsumptionNum, '0.2f')
        if koubei.fuelconsumption > strengthsValue:
            strengthsValue = koubei.fuelconsumption
            strengths = 'Fuel Consumption'
        if koubei.fuelconsumption < weaknessesValue:
            weaknessesValue = koubei.fuelconsumption
            weaknesses = 'Fuel Consumption'
    else:
        koubei.fuelconsumption = 0

    if interiorNum > 0:
        koubei.interior = format(koubei.interior / interiorNum, '0.2f')
        if koubei.interior > strengthsValue:
            strengthsValue = koubei.interior
            strengths = 'Interior'
        if koubei.interior < weaknessesValue:
            weaknessesValue = koubei.interior
            weaknesses = 'Interior'
    else:
        koubei.interior = 0

    if maneuverabilityNum > 0:
        koubei.maneuverability = format(koubei.maneuverability / maneuverabilityNum, '0.2f')
        if koubei.maneuverability > strengthsValue:
            strengthsValue = koubei.maneuverability
            strengths = 'Maneuverability'
        if koubei.maneuverability < weaknessesValue:
            weaknessesValue = koubei.maneuverability
            weaknesses = 'Maneuverability'
    else:
        koubei.maneuverability = 0

    if optionsandfeaturesNum > 0:
        koubei.optionsandfeatures = format(koubei.optionsandfeatures / optionsandfeaturesNum, '0.2f')
        if koubei.optionsandfeatures > strengthsValue:
            strengthsValue = koubei.optionsandfeatures
            strengths = 'Options/Features'
        if koubei.optionsandfeatures < weaknessesValue:
            weaknessesValue = koubei.optionsandfeatures
            weaknesses = 'Options/Features'
    else:
        koubei.optionsandfeatures = 0

    if overallNum > 0:
        koubei.overall = format(koubei.overall / overallNum, '0.2f')
    else:
        koubei.overall = 0

    if powerNum > 0:
        koubei.power = format(koubei.power / powerNum, '0.2f')
        if koubei.power > strengthsValue:
            strengthsValue = koubei.power
            strengths = 'Power'
        if koubei.power < weaknessesValue:
            weaknessesValue = koubei.power
            weaknesses = 'Power'
    else:
        koubei.power = 0

    if valueformoneyNum > 0:
        koubei.valueformoney = format(koubei.valueformoney / valueformoneyNum, '0.2f')
        if koubei.valueformoney > strengthsValue:
            strengthsValue = koubei.valueformoney
            strengths = 'Valueformoney'
        if koubei.valueformoney < weaknessesValue:
            weaknessesValue = koubei.valueformoney
            weaknesses = 'Valueformoney'
    else:
        koubei.valueformoney = 0

    koubei.createdate = data[0][13]
    koubei.strengths = strengths
    koubei.weaknesses = weaknesses
    koubei.datanum = len(data)


    return koubei

# 处理返回excel的数据
def returnKoubeiExcel(data):
    output = BytesIO()  # 在内存中创建一个缓存流
    workbook = xlsxwriter.Workbook(output)
    worksheet = workbook.add_worksheet()

    # 设置表头
    worksheet.write(0, 0, 'brand')
    worksheet.write(0, 1, 'name')
    worksheet.write(0, 2, 'model')
    worksheet.write(0, 3, 'carseries')
    worksheet.write(0, 4, 'overall')
    worksheet.write(0, 5, 'exterior')
    worksheet.write(0, 6, 'interior')
    worksheet.write(0, 7, 'carspace')

    worksheet.write(0, 8, 'valueformoney')
    worksheet.write(0, 9, 'power')
    worksheet.write(0, 10, 'maneuverability')
    worksheet.write(0, 11, 'fuelConsumption')
    worksheet.write(0, 12, 'comfort')
    worksheet.write(0, 13, 'optionsandfeatures')
    worksheet.write(0, 14, 'createdate')
    worksheet.write(0, 15, 'source')
    worksheet.write(0, 16, 'comment')

    # 设置值
    row = 0
    for item in data:
        row += 1
        worksheet.write(row, 0, item[1])
        worksheet.write(row, 1, item[2])
        worksheet.write(row, 2, item[3])
        worksheet.write(row, 3, item[4])
        worksheet.write(row, 4, item[5])
        worksheet.write(row, 5, item[6])
        worksheet.write(row, 6, item[7])
        worksheet.write(row, 7, item[8])

        worksheet.write(row, 8, item[9])
        worksheet.write(row, 9, item[10])
        worksheet.write(row, 10, item[11])
        worksheet.write(row, 11, item[12])
        worksheet.write(row, 12, item[13])
        worksheet.write(row, 13, item[14])
        worksheet.write(row, 14, item[15])
        worksheet.write(row, 15, item[16])
        worksheet.write(row, 16, item[17])

    workbook.close()
    output.seek(0)

    headers = {
        'Content-Disposition': 'attachment; filename="filename.xlsx"'
    }
    return output, headers

# 引入 textNN/deal_comment 中nlp函数处理，比较慢
def deal_comment_percent_test(data):
    commentPer = koubeiCommentPer()

    if (len(data) == 0):
        return commentPer

    for item in data:
        overall = item[0]
        exterior = item[1]
        interior = item[2]
        carSpace = item[3]
        valueformoney = item[4]
        power = item[5]
        maneuverability = item[6]
        fuelConsumption = item[7]
        comfort = item[8]
        optionsandfeatures = item[9]

        res = overall.replace('，', '。').split('。')
        for item1 in res:
            if item1 == "":
                continue
            commentPer.overall = commentPer.overall + 1
            atti = predict_zfz(item1)
            if atti == 1:
                commentPer.overallPositive = commentPer.overallPositive + 1
            elif atti == 0:
                commentPer.overallNeutral = commentPer.overallNeutral + 1
            else:
                commentPer.overallNegitive = commentPer.overallNegitive + 1

        res = exterior.replace('，', '。').split('。')
        for item1 in res:
            if item1 == "":
                continue
            commentPer.exterior = commentPer.exterior + 1
            atti = predict_zfz(item1)
            if atti == 1:
                commentPer.exteriorPositive = commentPer.exteriorPositive + 1
            elif atti == 0:
                commentPer.exteriorNeutral = commentPer.exteriorNeutral + 1
            else:
                commentPer.exteriorNegitive = commentPer.exteriorNegitive + 1

        res = interior.replace('，', '。').split('。')
        for item1 in res:
            if item1 == "":
                continue
            commentPer.interior = commentPer.interior + 1
            atti = predict_zfz(item1)
            if atti == 1:
                commentPer.interiorPositive = commentPer.interiorPositive + 1
            elif atti == 0:
                commentPer.interiorNeutral = commentPer.interiorNeutral + 1
            else:
                commentPer.interiorNegitive = commentPer.interiorNegitive + 1

        res = carSpace.replace('，', '。').split('。')
        for item1 in res:
            if item1 == "":
                continue
            commentPer.carspace = commentPer.carspace + 1
            atti = predict_zfz(item1)
            if atti == 1:
                commentPer.carspacePositive = commentPer.carspacePositive + 1
            elif atti == 0:
                commentPer.carspaceNeutral = commentPer.carspaceNeutral + 1
            else:
                commentPer.carspaceNegitive = commentPer.carspaceNegitive + 1

        res = valueformoney.replace('，', '。').split('。')
        for item1 in res:
            if item1 == "":
                continue
            commentPer.valueformoney = commentPer.valueformoney + 1
            atti = predict_zfz(item1)
            if atti == 1:
                commentPer.valueformoneyPositive = commentPer.valueformoneyPositive + 1
            elif atti == 0:
                commentPer.valueformoneNeutral = commentPer.valueformoneNeutral + 1
            else:
                commentPer.valueformoneNegitive = commentPer.valueformoneNegitive + 1

        res = power.replace('，', '。').split('。')
        for item1 in res:
            if item1 == "":
                continue
            commentPer.power = commentPer.power + 1
            atti = predict_zfz(item1)
            if atti == 1:
                commentPer.powerPositive = commentPer.powerPositive + 1
            elif atti == 0:
                commentPer.powerNeutral = commentPer.powerNeutral + 1
            else:
                commentPer.powerNegitive = commentPer.powerNegitive + 1

        res = maneuverability.replace('，', '。').split('。')
        for item1 in res:
            if item1 == "":
                continue
            commentPer.maneuverability = commentPer.maneuverability + 1
            atti = predict_zfz(item1)
            if atti == 1:
                commentPer.maneuverabilityPositive = commentPer.maneuverabilityPositive + 1
            elif atti == 0:
                commentPer.maneuverabilityNeutral = commentPer.maneuverabilityNeutral + 1
            else:
                commentPer.maneuverabilityNegitive = commentPer.maneuverabilityNegitive + 1

        res = fuelConsumption.replace('，', '。').split('。')
        for item1 in res:
            if item1 == "":
                continue
            commentPer.fuelConsumption = commentPer.fuelConsumption + 1
            atti = predict_zfz(item1)
            if atti == 1:
                commentPer.fuelConsumptionPositive = commentPer.fuelConsumptionPositive + 1
            elif atti == 0:
                commentPer.fuelConsumptionNeutral = commentPer.fuelConsumptionNeutral + 1
            else:
                commentPer.fuelConsumptionNegitive = commentPer.fuelConsumptionNegitive + 1

        res = comfort.replace('，', '。').split('。')
        for item1 in res:
            if item1 == "":
                continue
            commentPer.comfort = commentPer.comfort + 1
            atti = predict_zfz(item1)
            if atti == 1:
                commentPer.comfortPositive = commentPer.comfortPositive + 1
            elif atti == 0:
                commentPer.comfortNeutral = commentPer.comfortNeutral + 1
            else:
                commentPer.comfortNegitive = commentPer.comfortNegitive + 1

        res = optionsandfeatures.replace('，', '。').split('。')
        for item1 in res:
            if item1 == "":
                continue
            commentPer.optionsandfeatures = commentPer.optionsandfeatures + 1
            atti = predict_zfz(item1)
            if atti == 1:
                commentPer.optionsandfeaturesPositive = commentPer.optionsandfeaturesPositive + 1
            elif atti == 0:
                commentPer.optionsandfeaturesNeutral = commentPer.optionsandfeaturesNeutral + 1
            else:
                commentPer.optionsandfeaturesNegitive = commentPer.optionsandfeaturesNegitive + 1

    return commentPer

# 直接在这里写nlp的代码
def deal_comment_percent(data):
    commentPer = koubeiCommentPer()

    if (len(data) == 0):
        return commentPer

    # nlp
    file_os = os.path.dirname(__file__)
    with open(os.path.join(file_os, '../textNN/model/zfz_vocab_new'), 'rb') as f:
        vocab = dill.load(f)
        RNNnet = lsRNN(vocab, 50, 100, 2)
        RNNnet.load_state_dict(
            torch.load(os.path.join(file_os, '../textNN/model/Emotion_classification_zfz_new.pth'), map_location='cpu'))
        RNNnet.eval()

        for item in data:
            if item[0] == None:
                continue
            overall = item[0]
            exterior = item[1]
            interior = item[2]
            carSpace = item[3]
            valueformoney = item[4]
            power = item[5]
            maneuverability = item[6]
            fuelConsumption = item[7]
            comfort = item[8]
            optionsandfeatures = item[9]

            res = overall.replace('，', '。').split('。')
            for item1 in res:
                if item1 == "":
                    continue
                commentPer.overall = commentPer.overall + 1

                data = [[item1, 1]]
                x, _ = preprocess(data, vocab)

                with torch.no_grad():
                    label = torch.argmax(RNNnet(x), dim=1)
                atti = label.item() - 1

                if atti == 1:
                    commentPer.overallPositive = commentPer.overallPositive + 1
                elif atti == 0:
                    commentPer.overallNeutral = commentPer.overallNeutral + 1
                else:
                    commentPer.overallNegitive = commentPer.overallNegitive + 1

            res = exterior.replace('，', '。').split('。')
            for item1 in res:
                if item1 == "":
                    continue
                commentPer.exterior = commentPer.exterior + 1

                data = [[item1, 1]]
                x, _ = preprocess(data, vocab)

                with torch.no_grad():
                    label = torch.argmax(RNNnet(x), dim=1)
                atti = label.item() - 1

                if atti == 1:
                    commentPer.exteriorPositive = commentPer.exteriorPositive + 1
                elif atti == 0:
                    commentPer.exteriorNeutral = commentPer.exteriorNeutral + 1
                else:
                    commentPer.exteriorNegitive = commentPer.exteriorNegitive + 1

            res = interior.replace('，', '。').split('。')
            for item1 in res:
                if item1 == "":
                    continue
                commentPer.interior = commentPer.interior + 1

                data = [[item1, 1]]
                x, _ = preprocess(data, vocab)

                with torch.no_grad():
                    label = torch.argmax(RNNnet(x), dim=1)
                atti = label.item() - 1

                if atti == 1:
                    commentPer.interiorPositive = commentPer.interiorPositive + 1
                elif atti == 0:
                    commentPer.interiorNeutral = commentPer.interiorNeutral + 1
                else:
                    commentPer.interiorNegitive = commentPer.interiorNegitive + 1

            res = carSpace.replace('，', '。').split('。')
            for item1 in res:
                if item1 == "":
                    continue
                commentPer.carspace = commentPer.carspace + 1

                data = [[item1, 1]]
                x, _ = preprocess(data, vocab)

                with torch.no_grad():
                    label = torch.argmax(RNNnet(x), dim=1)
                atti = label.item() - 1

                if atti == 1:
                    commentPer.carspacePositive = commentPer.carspacePositive + 1
                elif atti == 0:
                    commentPer.carspaceNeutral = commentPer.carspaceNeutral + 1
                else:
                    commentPer.carspaceNegitive = commentPer.carspaceNegitive + 1

            res = valueformoney.replace('，', '。').split('。')
            for item1 in res:
                if item1 == "":
                    continue
                commentPer.valueformoney = commentPer.valueformoney + 1

                data = [[item1, 1]]
                x, _ = preprocess(data, vocab)

                with torch.no_grad():
                    label = torch.argmax(RNNnet(x), dim=1)
                atti = label.item() - 1

                if atti == 1:
                    commentPer.valueformoneyPositive = commentPer.valueformoneyPositive + 1
                elif atti == 0:
                    commentPer.valueformoneyNeutral = commentPer.valueformoneyNeutral + 1
                else:
                    commentPer.valueformoneyNegitive = commentPer.valueformoneyNegitive + 1

            res = power.replace('，', '。').split('。')
            for item1 in res:
                if item1 == "":
                    continue
                commentPer.power = commentPer.power + 1

                data = [[item1, 1]]
                x, _ = preprocess(data, vocab)

                with torch.no_grad():
                    label = torch.argmax(RNNnet(x), dim=1)
                atti = label.item() - 1

                if atti == 1:
                    commentPer.powerPositive = commentPer.powerPositive + 1
                elif atti == 0:
                    commentPer.powerNeutral = commentPer.powerNeutral + 1
                else:
                    commentPer.powerNegitive = commentPer.powerNegitive + 1

            res = maneuverability.replace('，', '。').split('。')
            for item1 in res:
                if item1 == "":
                    continue
                commentPer.maneuverability = commentPer.maneuverability + 1

                data = [[item1, 1]]
                x, _ = preprocess(data, vocab)

                with torch.no_grad():
                    label = torch.argmax(RNNnet(x), dim=1)
                atti = label.item() - 1

                if atti == 1:
                    commentPer.maneuverabilityPositive = commentPer.maneuverabilityPositive + 1
                elif atti == 0:
                    commentPer.maneuverabilityNeutral = commentPer.maneuverabilityNeutral + 1
                else:
                    commentPer.maneuverabilityNegitive = commentPer.maneuverabilityNegitive + 1

            res = fuelConsumption.replace('，', '。').split('。')
            for item1 in res:
                if item1 == "":
                    continue
                commentPer.fuelConsumption = commentPer.fuelConsumption + 1

                data = [[item1, 1]]
                x, _ = preprocess(data, vocab)

                with torch.no_grad():
                    label = torch.argmax(RNNnet(x), dim=1)
                atti = label.item() - 1

                if atti == 1:
                    commentPer.fuelConsumptionPositive = commentPer.fuelConsumptionPositive + 1
                elif atti == 0:
                    commentPer.fuelConsumptionNeutral = commentPer.fuelConsumptionNeutral + 1
                else:
                    commentPer.fuelConsumptionNegitive = commentPer.fuelConsumptionNegitive + 1

            res = comfort.replace('，', '。').split('。')
            for item1 in res:
                if item1 == "":
                    continue
                commentPer.comfort = commentPer.comfort + 1

                data = [[item1, 1]]
                x, _ = preprocess(data, vocab)

                with torch.no_grad():
                    label = torch.argmax(RNNnet(x), dim=1)
                atti = label.item() - 1

                if atti == 1:
                    commentPer.comfortPositive = commentPer.comfortPositive + 1
                elif atti == 0:
                    commentPer.comfortNeutral = commentPer.comfortNeutral + 1
                else:
                    commentPer.comfortNegitive = commentPer.comfortNegitive + 1

            res = optionsandfeatures.replace('，', '。').split('。')
            for item1 in res:
                if item1 == "":
                    continue
                commentPer.optionsandfeatures = commentPer.optionsandfeatures + 1

                data = [[item1, 1]]
                x, _ = preprocess(data, vocab)

                with torch.no_grad():
                    label = torch.argmax(RNNnet(x), dim=1)
                atti = label.item() - 1

                if atti == 1:
                    commentPer.optionsandfeaturesPositive = commentPer.optionsandfeaturesPositive + 1
                elif atti == 0:
                    commentPer.optionsandfeaturesNeutral = commentPer.optionsandfeaturesNeutral + 1
                else:
                    commentPer.optionsandfeaturesNegitive = commentPer.optionsandfeaturesNegitive + 1

    # 用平均值
    if commentPer.overall != 0:
        commentPer.overallPositive = int(commentPer.overallPositive / commentPer.overall * 100)
        commentPer.overallNeutral = int(commentPer.overallNeutral / commentPer.overall * 100)
        commentPer.overallNegitive = 100 - commentPer.overallPositive - commentPer.overallNeutral

    if commentPer.exterior != 0:
        commentPer.exteriorPositive = int(commentPer.exteriorPositive / commentPer.exterior * 100)
        commentPer.exteriorNeutral = int(commentPer.exteriorNeutral / commentPer.exterior * 100)
        commentPer.exteriorNegitive = 100 - commentPer.exteriorPositive - commentPer.exteriorNeutral

    if commentPer.interior != 0:
        commentPer.interiorPositive = int(commentPer.interiorPositive / commentPer.interior * 100)
        commentPer.interiorNeutral = int(commentPer.interiorNeutral / commentPer.interior * 100)
        commentPer.interiorNegitive = 100 - commentPer.interiorPositive - commentPer.interiorNeutral

    if commentPer.carspace != 0:
        commentPer.carspacePositive = int(commentPer.carspacePositive / commentPer.carspace * 100)
        commentPer.carspaceNeutral = int(commentPer.carspaceNeutral / commentPer.carspace * 100)
        commentPer.carspaceNegitive = 100 - commentPer.carspacePositive - commentPer.carspaceNeutral

    if commentPer.valueformoney != 0:
        commentPer.valueformoneyPositive = int(commentPer.valueformoneyPositive / commentPer.valueformoney * 100)
        commentPer.valueformoneyNeutral = int(commentPer.valueformoneyNeutral / commentPer.valueformoney * 100)
        commentPer.valueformoneyNegitive = 100 - commentPer.valueformoneyPositive - commentPer.valueformoneyNeutral

    if commentPer.power != 0:
        commentPer.powerPositive = int(commentPer.powerPositive / commentPer.power * 100)
        commentPer.powerNeutral = int(commentPer.powerNeutral / commentPer.power * 100)
        commentPer.powerNegitive = 100 - commentPer.powerPositive - commentPer.powerNeutral

    if commentPer.maneuverability != 0:
        commentPer.maneuverabilityPositive = int(commentPer.maneuverabilityPositive / commentPer.maneuverability * 100)
        commentPer.maneuverabilityNeutral = int(commentPer.maneuverabilityNeutral / commentPer.maneuverability * 100)
        commentPer.maneuverabilityNegitive = 100 - commentPer.maneuverabilityPositive - commentPer.maneuverabilityNeutral

    if commentPer.fuelConsumption != 0:
        commentPer.fuelConsumptionPositive = int(commentPer.fuelConsumptionPositive / commentPer.fuelConsumption * 100)
        commentPer.fuelConsumptionNeutral = int(commentPer.fuelConsumptionNeutral / commentPer.fuelConsumption * 100)
        commentPer.fuelConsumptionNegitive = 100 - commentPer.fuelConsumptionPositive - commentPer.fuelConsumptionNeutral

    if commentPer.comfort != 0:
        commentPer.comfortPositive = int(commentPer.comfortPositive / commentPer.comfort * 100)
        commentPer.comfortNeutral = int(commentPer.comfortNeutral / commentPer.comfort * 100)
        commentPer.comfortNegitive = 100 - commentPer.comfortPositive - commentPer.comfortNeutral

    if commentPer.optionsandfeatures != 0:
        commentPer.optionsandfeaturesPositive = int(commentPer.optionsandfeaturesPositive / commentPer.optionsandfeatures * 100)
        commentPer.optionsandfeaturesNeutral = int(commentPer.optionsandfeaturesNeutral / commentPer.optionsandfeatures * 100)
        commentPer.optionsandfeaturesNegitive = 100 - commentPer.optionsandfeaturesPositive - commentPer.optionsandfeaturesNeutral



    return commentPer

if __name__ == '__main__':
    strs = "12321,fsafs.42423"
    res = strs.split(',')
    print(res)


