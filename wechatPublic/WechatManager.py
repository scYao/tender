# coding=utf8
import hashlib
import json
import urllib
from tool.Util import Util

class WechatManager(Util):
    def __init__(self):
        self.appID = 'wxe56d1e66d153e211'
        self.appSecret = 'ec37ced1ae89e57b250ac43493124823'
        self.accessToken = ''

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
        accessToken = self.getAccessToken()
        postUrl = "https://api.weixin.qq.com/cgi-bin/menu/create?access_token=%s" % accessToken
        if isinstance(postData, unicode):
            postData = postData.encode('utf-8')
        urlResp = urllib.urlopen(url=postUrl, data=postData)
        print urlResp.read()

    #发送模板信息
    def pushTemplateMessage(self, postData):
        accessToken = self.getAccessToken()
        postUrl = "https://api.weixin.qq.com/cgi-bin/message/template/send?access_token=%s" % accessToken
        if isinstance(postData, unicode):
            postData = postData.encode('utf-8')
        urlResp = urllib.urlopen(url=postUrl, data=postData)
        print urlResp.read()


    #test celery
    def testCelery(self):
        # add.delay(22, 33)
        return 'hello, sunshine!'


if __name__ == '__main__':
    weChatManager = WechatManager()
    weChatManager.getUserList()
    # weChatManager.testCelery()
    # wechatPublic.getOpenID()
    # wechatPublic.getAccessToken()
    # postData = """{
    #     "touser": "o-U_Uwi9_kk_WeqO57nZI8SB0aiI",
    #     "template_id": "fITnnxJK2p903OFmvIVEhNzw4kDVJ1z8tE3FYfs0cts",
    #     "url": "https://open.weixin.qq.com/connect/oauth2/authorize?appid=wxe56d1e66d153e211&redirect_uri=http://1b6d01ea.ngrok.io/callback/&response_type=code&scope=snsapi_base&state=123#wechat_redirect",
    #     "data":{}
    # }
    # """
    # wechatPublic.pushTemplateMessage(postData=postData)
    # postData = """
    #   {
    #       "button":
    #       [
    #           {
    #            "type":"view",
    #            "name":"搜索",
    #            "url":"http://mp.weixin.qq.com"
    #           },
    #           {
    #              "type":"view",
    #              "name":"订阅",
    #              "url":"http://www.soso.com/"
    #           },
    #           {
    #               "name": "关于",
    #               "sub_button":
    #               [
    #                   {
    #                      "type":"view",
    #                      "name":"关于我们",
    #                      "url":"http://www.soso.com/"
    #                   },
    #                   {
    #                       "type": "view",
    #                       "name": "使用技巧",
    #                       "url": "http://mp.weixin.qq.com/wiki?t=resource/res_main&id=mp1418702138&token=&lang=zh_CN"
    #                   },
    #                   {
    #                       "type": "view",
    #                       "name": "意见反馈",
    #                       "url": "http://mp.weixin.qq.com/wiki?t=resource/res_main&id=mp1433747234&token=&lang=zh_CN"
    #                   }
    #               ]
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
