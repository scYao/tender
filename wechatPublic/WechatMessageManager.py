# coding=utf8
from tool.Util import Util

class WechatMessageManager(Util):

    def __init__(self):
        pass

    #接收消息
    def getMessageInfo(self, xmlData):
        (status, messageInfo) = self.parseXmlData(xmlData)
        if status == True:
            type = messageInfo['megType']
            if type == 'text':
                messageInfo['content'] = '112'
                return self.sendTextMessage(info=messageInfo)
            elif type == 'event':
                if messageInfo['event'] == 'subscribe':
                    messageInfo['content'] = '欢迎订阅！'
                    return self.sendTextMessage(info=messageInfo)
            return 'success'
        else:
            return 'success'



if __name__ == '__main__':
    pass

