import jieba
import arrow
import pymysql
from models.weiboHuati import *
from textNN.deal_comment import *

" 查询目前为止100天的日期，不包括当天，从前一天开始 "
def query_100_days_datas():
    returnData = []
    # 1. 获取目前位置100天的日期
    # 1.1 获取当天日期
    current_date = arrow.now()
    for i in range(0, 100):
        last_days = current_date.shift(days = 0 - i - 1).strftime("%Y-%m-%d")
        returnData.append(last_days)
    return returnData

def searchAllByTime(dates: str):
    """
       :param dates: 日期
       :return: 返回所有品牌一周内，话题评论最多的三个帖子
    """
    " 如果日期为空，则默认前一天的日期 "
    if dates:
        dates = dates
    else:
        dates = arrow.now().shift(days=- 1).strftime("%Y-%m-%d")

    " 获取这个7天的时间段 "
    begin_date = arrow.get(dates).shift(days=-6).strftime("%Y-%m-%d")
    end_date = arrow.get(dates).shift(days=1).strftime("%Y-%m-%d")
    # 1 连接数据库
    conn = pymysql.connect(host='localhost', user='root', passwd='12345678', db='showcar', charset="utf8")
    cur = conn.cursor()
    " 1. 有几个品牌 "
    sql = "select distinct brand from officialweibo"
    cur.execute(sql)
    result = cur.fetchall()
    brands = []
    for i in range(0, len(result)):
        brands.append(result[i][0])
    " 2. 查询所有品牌一周内，话题最多的三个帖子 "
    returnData = []
    for i in range(0, len(brands)):
        sql = "select * from topicpost where brand = (%s) and time > (%s) and time < (%s) order by commentscount desc limit 0, 3"
        cur.execute(sql, (brands[i], begin_date, end_date))
        result = cur.fetchall()
        for item in result:
            topicPost = TopicPost()
            topicPost.brand = item[1]
            topicPost.text = item[2]
            topicPost.linkurl = item[3]
            topicPost.timestring = str(item[4])[0: 10]
            topicPost.commentscount = item[5]
            topicPost.keywordsTimes = str(item[2]).count(brands[i])
            returnData.append(topicPost)

    " 3. 处理情感正负性 "
    " 3.1 连接npl "
    file_os = os.path.dirname(__file__)
    with open(os.path.join(file_os, '../textNN/model/zfz_vocab_new'), 'rb') as f:
        vocab = dill.load(f)
        RNNnet = lsRNN(vocab, 50, 100, 2)
        RNNnet.load_state_dict(
            torch.load(os.path.join(file_os, '../textNN/model/Emotion_classification_zfz_new.pth'), map_location='cpu'))
        RNNnet.eval()
        " 3.2 循环处理 "
        for i in range(0, len(returnData)):
            data = [[returnData[i].text, 1]]
            x, _ = preprocess(data, vocab)
            with torch.no_grad():
                label = torch.argmax(RNNnet(x), dim=1)
            att = label.item()
            if att == 0:
                returnData[i].emotion = '负'
            elif att == 1:
                returnData[i].emotion = '中'
            else:
                returnData[i].emotion = '正'

    # 关闭数据库
    cur.close()
    conn.commit()
    conn.close()
    return returnData

" 返回某个品牌话题的 关注量、粉丝、帖子数量、爬取时间 "
def searchUserInfo(brand: str, date: str):
    # 1 连接数据库
    conn = pymysql.connect(host='localhost', user='root', passwd='12345678', db='showcar', charset="utf8")
    cur = conn.cursor()
    returnData = WeiboTopic()
    if date:
        date = date
    else:
        current_date = arrow.now()
        date = current_date.shift(days = -1).strftime("%Y-%m-%d")
    sql = "select * FROM weibotopic WHERE topicname = (%s) and time like (%s)"
    cur.execute(sql, (brand, date + '%'))
    result = cur.fetchall()
    if len(result) == 0:
        returnData.topicname = brand
        returnData.readingnum = ''
        returnData.discussionnum = ''
        returnData.timestring = ''
    else:
        returnData.topicname = result[0][1]
        returnData.readingnum = result[0][2]
        returnData.discussionnum = result[0][3]
        returnData.timestring = str(result[0][4])[0: 10]

        # 关闭数据库
    cur.close()
    conn.commit()
    conn.close()

    return returnData

def searchWordCloudData(brand: str, date: str):
    if date:
        date = date
    else:
        current_date = arrow.now()
        date = current_date.shift(days = -1).strftime("%Y-%m-%d")
    # 1 连接数据库
    conn = pymysql.connect(host='localhost', user='root', passwd='12345678', db='showcar', charset="utf8")
    cur = conn.cursor()

    " 2. 按条件查找所有数据 "
    sql = "select text from topicpost where brand = (%s) and time like (%s)"
    cur.execute(sql, (brand, date + '%'))
    result = cur.fetchall()

    " 3. 对每条数据进行分词，并且加入到分词列表中存储"
    wordList = {}
    for i in range(len(result)):
        # 3.1 对每个text进行分词
        jiebaList = jieba.cut(result[i][0], cut_all=False)
        deleteWords = ['的', '了', '吗', '你', '我', '怎么', '吧', '这', '了吗', '还', '这个', '那个', '什么']
        # 3.2 将分词的结果遍历
        for item in jiebaList:
            if is_Chinese(item):
                if item in deleteWords:
                    continue
                if (wordList.get(item)):
                    wordList[item] = wordList[item] + 1
                else:
                    wordList[item] = 1
    "4. 将wordlist排序"
    wordList_tuplelist = list(zip(wordList.values(), wordList.keys()))
    wordList_sorted = sorted(wordList_tuplelist, reverse=True)
    " 5. 将前 180 个键值对转化为WordCloud，因为超过180 前端展示不了 "
    returnData = []
    length = min(len(wordList_sorted), 180)
    for i in range(0, length):
        wordCloud = WordCloud()
        wordCloud.name = wordList_sorted[i][1]
        wordCloud.value = wordList_sorted[i][0]
        returnData.append(wordCloud)

    # 关闭数据库
    cur.close()
    conn.commit()
    conn.close()

    " 5. 返回分词列表 "
    return returnData


" 判断字符串是否全是中文 "
def is_Chinese(word: str):
    if word == '':
        return False
    for i in range(0, len(word)):
        if word[i] < '\u4e00' or word[i] > '\u9fff':
            return False
    return True

if __name__ == '__main__':
    searchAllByTime('')