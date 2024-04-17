import arrow

class RetunDataOfByBrand():
    def __init__(self):
        self.id = 0
        self.brand = ''
        self.englishBrand = ''
        self.carseries = ''
        self.buyyear = ''
        self.buymonth = ''
        self.englishbuymonth = ''
        self.discount = ''

if __name__ == '__main__':
    returnData = []
    current_date = arrow.now()
    for i in range(0, 12):
        last_month = current_date.shift(months = 0 - i).strftime("%Y-%m-%d")
        dis = RetunDataOfByBrand()
        dis.buyyear = last_month[0: 4]
        dis.buymonth = last_month[5: 7]
        returnData.append(dis)

    for i in range(0, 12):
        print(returnData[i].buymonth)
