# coding=utf8
import hashlib
import json
import urllib
from tool.Util import Util
from tool.tagconfig import PUBLICAPPID
from tool.tagconfig import PUBLICSECRET
from models.flask_app import db
from models.UserInfo import UserInfo
from models.Tender import Tender
from models.WeChatPush import WeChatPush
from models.WeChatPushHistory import WeChatPushHistory
from datetime import datetime
from models.UserInfo import UserInfo
from models.City import City
from models.Province import Province
from models.Tender import Tender
from models.WinBiddingPub import WinBiddingPub
from models.UserIP import UserIP
from models.Candidate import Candidate
from models.SubscribedKey import SubscribedKey
from models.WeChatPushHistory import WeChatPushHistory
from models.Favorite import Favorite
from models.Token import Token
from models.WeChatPush import WeChatPush
from models.SearchKey import SearchKey
from models.flask_app import db
from tool.Util import Util
from tool.tagconfig import TEMPLATEID, MINIAPPID, SEARCH_KEY_TAG_SUBSCRIBE
from sqlalchemy import and_


class WechatManager(Util):
    def __init__(self):
        self.appID = 'wxe56d1e66d153e211'
        self.appSecret = 'ec37ced1ae89e57b250ac43493124823'
        # self.appID = 'wx6b06cac8fee40771'
        # self.appSecret = 'd6e12e186ec9e1dbf756f5cb3395b622'
        # self.appID = PUBLICAPPID
        # self.appSecret = PUBLICSECRET

    #获取用户基本信息
    def getUserInfo(self, openID):
        (status, accessToken) = self.getAccessToken()
        postUrl = ("https://api.weixin.qq.com/cgi-bin/user/info?access_token=%s&openid=%s&lang=zh_CN" % (
            accessToken, openID
        ))
        urlResp = urllib.urlopen(postUrl)
        urlResp = json.loads(urlResp.read())
        return (True, urlResp)

    #获取用户信息的回调函数
    def callBack(self, jsonInfo):
        info = json.loads(jsonInfo)
        code = info['code']
        grant_type = 'authorization_code'
        postUrl = ("https://api.weixin.qq.com/sns/oauth2/access_token?appid=%s&secret=%s&code=%s&grant_type=%s" %
                   (self.appID, self.appSecret, code, grant_type))
        urlResp = urllib.urlopen(postUrl)
        urlResp = json.loads(urlResp.read())
        return (True, 'hello, sunshine!')

    #获取用户列表
    def wxGetUserInfoList(self, jsonInfo):
        (status, accessToken) = self.getAccessToken()
        if status is True:
            postUrl = ("https://api.weixin.qq.com/cgi-bin/user/get?access_token=%s" % accessToken)
            urlResp = urllib.urlopen(postUrl)
            urlResp = json.loads(urlResp.read())
            return (True, urlResp)
        else:
            return (False, None)

    #验证服务合法性
    def login(self, jsonInfo):
        info = json.loads(jsonInfo)
        try:
            signature = info['signature']
            timestamp = info['timestamp']
            nonce = info['nonce']
            echostr = info['echostr']
            token = "kuafu" #请按照公众平台官网\基本配置中信息填写
            list = [token, timestamp, nonce]
            list.sort()
            sha1 = hashlib.sha1()
            map(sha1.update, list)
            hashcode = sha1.hexdigest()
            if hashcode == signature:
                return (True, echostr)
            else:
                return (False, None)
        except Exception, Argument:
            return (False, Argument)

    #自定义菜单
    def createMenu(self, postData):
        (status, accessToken) = self.getAccessToken()
        print status, accessToken
        postUrl = "https://api.weixin.qq.com/cgi-bin/menu/create?access_token=%s" % accessToken
        if isinstance(postData, unicode):
            postData = postData.encode('utf-8')
        urlResp = urllib.urlopen(url=postUrl, data=postData)
        print urlResp.read()

    #发送模板信息
    def pushTemplateMessage(self, postData):
        (status, accessToken) = self.getAccessToken()
        print status, accessToken
        postUrl = "https://api.weixin.qq.com/cgi-bin/message/template/send?access_token=%s" % accessToken
        if isinstance(postData, unicode):
            postData = postData.encode('utf-8')
        urlResp = urllib.urlopen(url=postUrl, data=postData)
        print urlResp.read()


    #测试推送完整消息
    def testPushTemplateMessage(self):
        (status, accessToken) = self.getAccessToken()
        # print status , accessToken
        query = db.session.query(
            WeChatPush, UserInfo, Tender
        ).outerjoin(
            UserInfo, WeChatPush.toUserID == UserInfo.userID
        ).outerjoin(
            Tender, WeChatPush.tenderID == Tender.tenderID
        )
        allResult = query.all()
        print len(allResult)
        postDic = {}

        def generate(result):
            userInfo = result.UserInfo
            tender = result.Tender
            userID = userInfo.openid1
            templateData = {}
            templateData['touser'] = userID
            templateData['userid'] = userInfo.userID
            templateData['template_id'] = 'fC0a2uChLx88d6PE51Le-9S3q9NcXN6k2hdqgpVwKE0'
            templateData['url'] = 'http://weixin.qq.com/download'
            templateData['remark'] = '  ' + tender.title + ';'  + '\n'
            if not postDic.has_key(userID):
                templateData['remark'] = '[1]  ' + templateData['remark']
                postDic[userID] = templateData
                postDic[userID]['count'] = 1
            else:
                postDic[userID]['count'] = postDic[userID]['count'] + 1
                # index = postDic[userID]['remark'].count(';')
                templateData['remark'] = '[' + str(postDic[userID]['count']) + ']  ' + templateData['remark']
                postDic[userID]['remark'] = postDic[userID]['remark'] + templateData['remark']

        [generate(result) for result in allResult]
        print '===', postDic, len(postDic)
        for key, value in postDic.iteritems():
            # print '----', value
            # 更新推送历史
            toUserID = value['userid']
            publishTime = datetime.now()
            pushQuery = db.session.query(WeChatPush).filter(
                WeChatPush.toUserID == toUserID
            )
            pushAllResult = pushQuery.all()
            for result in pushAllResult:
                createInfo = {}
                createInfo['pushedID'] = result.pushedID
                createInfo['tenderID'] = result.tenderID
                createInfo['toUserID'] = result.toUserID
                createInfo['createTime'] = result.createTime
                createInfo['publishTime'] = publishTime
                # WeChatPushHistory.create(createInfo=createInfo)
            # pushQuery.delete(synchronize_session=False)
            # db.session.commit()
            value['data'] = {
                "first": {
                    "value": "最新提醒！"
                },
                "keyword1": {
                    "value": "订阅提醒"
                },
                "keyword2": {
                    "value": "更新" + str(value['count']) + '条',
                },
                "remark": {
                    "value": value['remark'],
                    "color": "#1ebdff"
                }
            }
            # print value
            postData = json.dumps(value)
            postUrl = "https://api.weixin.qq.com/cgi-bin/message/template/send?access_token=%s" % accessToken
            urlResp = urllib.urlopen(url=postUrl, data=postData)
            print urlResp.read()
            return (True, None)
            # urlResp = json.loads(urlResp.read())
            # return (True, urlResp)


if __name__ == '__main__':
    weChatManager = WechatManager()
    weChatManager.testPushTemplateMessage()
    # testData = {
    #     '1' : '测试数据1',
    #     '2' : '测试数据2',
    #     '3' : '测试数据3',
    # }
    # postData = {}
    # postData['touser'] = 'o-U_Uwi9_kk_WeqO57nZI8SB0aiI'
    # postData['template_id'] = 'fC0a2uChLx88d6PE51Le-9S3q9NcXN6k2hdqgpVwKE0'
    # postData['data'] = {
    #     "first": {
    #         "value": "您的招标订阅有新消息！",
    #         "color": "#576b95"
    #     },
    #     "keyword1": {
    #         "value": "招标订阅"
    #     },
    #     "keyword2": {
    #         "value": "更新条数" + '3' + '条!',
    #     },
    #     "remark": {
    #         "value": '(1)' + '  测试数据1' + '\n' +  '(2)' + '  测试数据2' +  '\n' + '(3)' + '  测试数据3',
    #         "color": "#576b95"
    #     }
    # }
    # weChatManager.pushTemplateMessage(postData=json.dumps(postData))
    # weChatManager.getUserList()
    # weChatManager.testCelery()
    # wechatPublic.getOpenID()
    # wechatPublic.getAccessToken()
    # postData = """{
    #     "touser": "o-U_Uwi9_kk_WeqO57nZI8SB0aiI",
    #     "template_id": "fC0a2uChLx88d6PE51Le-9S3q9NcXN6k2hdqgpVwKE0",
    #     "url": "",
    #     "data":{
    #        "first": {
    #            "value":"恭喜你购买成功！",
    #            "color":"#173177"
    #        },
    #        "keynote1":{
    #            "value":"巧克力",
    #            "color":"#173177"
    #        },
    #        "keynote2": {
    #            "value":"39.8元",
    #            "color":"#173177"
    #        },
    #        "remark":{
    #            "value":"欢迎再次购买！",
    #            "color":"#173177"
    #        }
    #     }
    # }
    # """

    # postData = {}
    # postData['button'] = [
    #     {
    #         "type": "miniprogram",
    #         "name": "搜索",
    #         "url": "http://mp.weixin.qq.com",
    #         "appid": "wx3f8eb38c63060bf4",
    #         "pagepath": "pages/index/index"
    #     },
    #     {
    #         "type": "miniprogram",
    #         "name": "订阅",
    #         "url": "http://mp.weixin.qq.com",
    #         "appid": "wx3f8eb38c63060bf4",
    #         "pagepath": "pages/subscribe/subscribe"
    #     }
    # ]
    #
    # postData = """
    #   {
    #       "button":
    #       [
    #           {
    #             "type":"miniprogram",
    #             "name":"搜索",
    #             "url":"http://mp.weixin.qq.com",
    #             "appid":"wx3f8eb38c63060bf4",
    #             "pagepath":"pages/index/index"
    #           },
    #           {
    #             "type":"miniprogram",
    #             "name":"订阅",
    #             "url":"http://mp.weixin.qq.com",
    #             "appid":"wx3f8eb38c63060bf4",
    #             "pagepath":"pages/subscribe/subscribe"
    #           }
    #         ]
    #   }
    #   """
 #    postData = """
 #     {
 #     "button":[
 #     {
 #          "type":"click",
 #          "name":"今日歌曲",
 #          "key":"V1001_TODAY_MUSIC"
 #      },
 #      {
 #           "name":"菜单",
 #           "sub_button":[
 #           {
 #               "type":"view",
 #               "name":"搜索",
 #               "url":"http://www.soso.com/"
 #            },
 #            {
 #               "type":"click",
 #               "name":"赞一下我们",
 #               "key":"V1001_GOOD"
 #            }]
 #       }]
 # }
 #    """
 #    wechatPublic.createMenu(postData=postData)
 #    #
    #
