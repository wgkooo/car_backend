from pydantic import BaseModel
from typing import Optional


# class koubeiModel(BaseModel):
#     # id: Optional[int] = None # Optional 是设置可选
#     brand: str
#     model: str
#     name: str

class koubeiModel():
    def __init__(self):
        self.brand = ''
        self.model = ''
        self.name = ''

class koubeiReturnModel():
    def __init__(self):
        self.brand = ''
        self.model = ''
        self.name = ''
        self.carseries = ''
        self.carspace = 0.00
        self.comfort = 0.00
        self.exterior = 0.00
        self.fuelconsumption = 0.00
        self.interior = 0.00
        self.maneuverability = 0.00
        self.optionsandfeatures = 0.00
        self.overall = 0.00
        self.power = 0.00
        self.valueformoney = 0
        self.createdate = ''
        self.datanum = 0
        self.strengths = ''
        self.weaknesses = ''
        self.source = ''
        self.comment = ''

class koubeiCommentPer():
    def __init__(self):
        self.overallPositive = 0
        self.overallNegitive = 0
        self.overallNeutral = 0
        self.overall = 0

        self.exteriorPositive = 0
        self.exteriorNegitive = 0
        self.exteriorNeutral = 0
        self.exterior = 0

        self.interiorPositive = 0
        self.interiorNegitive = 0
        self.interiorNeutral = 0
        self.interior = 0

        self.carspacePositive = 0
        self.carspaceNegitive = 0
        self.carspaceNeutral = 0
        self.carspace = 0

        self.valueformoneyPositive = 0
        self.valueformoneyNegitive = 0
        self.valueformoneyNeutral = 0
        self.valueformoney = 0

        self.powerPositive = 0
        self.powerNegitive = 0
        self.powerNeutral = 0
        self.power = 0

        self.maneuverabilityPositive = 0
        self.maneuverabilityNegitive = 0
        self.maneuverabilityNeutral = 0
        self.maneuverability = 0

        self.fuelConsumptionPositive = 0
        self.fuelConsumptionNegitive = 0
        self.fuelConsumptionNeutral = 0
        self.fuelConsumption = 0

        self.comfortPositive = 0
        self.comfortNegitive = 0
        self.comfortNeutral = 0
        self.comfort = 0

        self.optionsandfeaturesPositive = 0
        self.optionsandfeaturesNegitive = 0
        self.optionsandfeaturesNeutral = 0
        self.optionsandfeatures = 0


if __name__ == '__main__':
    koube = koubeiReturnModel()
    print(koube.power)

