# coding=utf8
from tool.Util import Util
from celery_app import task1


class WechatMessageManager(Util):

    def __init__(self):
        pass

    #接收消息
    def getMessageInfo(self, xmlData):
        (status, messageInfo) = self.parseXmlData(xmlData)
        if status == True:
            type = messageInfo['megType']
            if type == 'text':
                messageInfo['content'] = '欢迎关注，(1)点击菜单中[搜索]可以查看招投标信息；(2)点击菜单中[订阅]可以实现招投标订阅功能！'
                return self.sendTextMessage(info=messageInfo)
            elif type == 'event':
                if messageInfo['event'] == 'subscribe':
                    task1.createUser.apply_async(args=[messageInfo])
                    messageInfo['content'] = '欢迎关注！'
                    return self.sendTextMessage(info=messageInfo)
                elif messageInfo['event'] == 'unsubscribe':
                    task1.deleteUser.apply_async(args=[messageInfo])
                    return 'success'
            return 'success'
        else:
            return 'success'




if __name__ == '__main__':
    pass

