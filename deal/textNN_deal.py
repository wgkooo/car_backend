import re
from dao.koubei import *
from textNN.deal_comment import *

def selectEmotionByBrandAndName_deal(data):

    comment = []
    # 1 把所有的评论合在一起
    for item in data:
        if item[14] != '' and item[14] != None:
            text = str(item[14]).replace('\n', '')
            p = re.compile(r'【.*?】')
            textSet = p.split(text)
            # 将textSet添加到comment中
            for item1 in textSet:
                if item1 != '':
                    comment.append(item1)

    # 2 按照句号分开
    newComment = []
    for item in comment:
        textContent = item

        # 将每个内容给细分
        p1 = re.compile(r'【.*?】')
        listContent = p1.split(textContent.replace('?', '【】').replace('。', '【】'))
        for item1 in listContent:
            if item1 != '':
                newComment.append(item1)

    # 3 测试每个评论，生成新的 newComments，每个元素为comment + -1/0/1
    # 4 统计总共有多少评论，以及正、负、中 的个数
    listPositiveNum = 0
    listNegativeNum = 0
    listMiddleNum = 0
    return dealComment(newComment)




if __name__ == '__main__':
    data = selectAllByNameAndDate_Dao('A4L', '2022-03-21')
    resultComment, listNegativeNum, listMiddleNum, listPositiveNum = selectEmotionByBrandAndName_deal(data)
    print(resultComment)
    print(listNegativeNum)
    print(listMiddleNum)
    print(listPositiveNum)

    comment = ''
    for item in resultComment:
        comment += item + '\n'
    print(comment)