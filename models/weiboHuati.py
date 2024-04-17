
class WeiboTopic():
    def __init__(self):
        self.id = ''
        self.topicname = ''
        self.readingnum = ''
        self.discussionnum = ''
        self.timestring = ''

class TopicPost():
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