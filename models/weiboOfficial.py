

class OfficialWeibo():
    def __init__(self):
        self.id = ''
        self.brand = ''
        self.followingnum = ''
        self.followednum = ''
        self.forumnum = ''
        self.timestring = ''

class OfficialPost():
    def __init__(self):
        self.id = ''
        self.brand = ''
        self.text = ''
        self.linkurl = ''
        self.timestring = ''
        self.commentscount = ''
        self.keywordsTimes = 0
        self.emotion = '中'

class WordCloud():
    def __init__(self):
        self.id = ''
        self.name = ''
        self.value = ''

if __name__ == '__main__':
    w = []
    w.append('123')
    w.append('3')
    print(w)