#coding: utf-8
import urllib
import json
from datetime import datetime
from celery_app import app
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
from wechatPublic.WechatManager import WechatManager
from tender.SubscribedKeyManager import SubscribedKeyManager
from tool.Util import Util
from tool.tagconfig import TEMPLATEID, MINIAPPID, SEARCH_KEY_TAG_SUBSCRIBE
from sqlalchemy import and_
from tool.config import ErrorInfo

#创建用户(公众号）
@app.task
def createUser(info):
    wechatManager = WechatManager()
    util = Util()
    openID = info['fromUserName']
    (status, userInfo) = wechatManager.getUserInfo(openID=openID)
    if status is True:
        try:
            unionid = util.generateUnionID(userInfo['nickname'])
            query = db.session.query(UserInfo).filter(UserInfo.unionid == unionid)
            result = query.first()
            userID = util.generateID(openID)
            createInfo = {}
            createInfo['userID'] = userID
            createInfo['userName'] = userInfo['nickname']
            createInfo['tel'] = ''
            createInfo['createTime'] = datetime.now()
            createInfo['openid1'] = openID
            createInfo['unionid'] = unionid
            if result is not None:
                #第一种情况，用户已经登录过小程序
                appUserID = result.userID
                openid2 = result.openid2
                #(0)创建新的用户记录
                createInfo['openid2'] = openid2
                UserInfo.createWeChat(createInfo=createInfo)
                #(1)变更Tender中userID
                # 速度太慢，暂时不修改。 若要绑定手机号，一手机号ID为主
                # db.session.query(Tender).filter(
                #     Tender.userID == appUserID
                # ).update({Token.userID: userID}, synchronize_session=False)
                #(2)变更订阅表subscribedKey中userID
                db.session.query(SubscribedKey).filter(
                    SubscribedKey.userID == appUserID
                ).update({SubscribedKey.userID: userID}, synchronize_session=False)
                #(3)变更关注表Favorite中的userID
                db.session.query(Favorite).filter(
                    Favorite.userID == appUserID
                ).update({Favorite.userID: userID}, synchronize_session=False)
                #(4)变更tokenID表中的userID
                db.session.query(Token).filter(
                    Token.userID == appUserID
                ).update({Token.userID: userID}, synchronize_session=False)
                # search key update
                db.session.query(SearchKey).filter(
                    and_(SearchKey.tag == SEARCH_KEY_TAG_SUBSCRIBE,
                         SearchKey.foreignID == appUserID)
                ).update({SearchKey.foreignID: userID}, synchronize_session=False)
                #(5)删除userInfo中的appUserID
                db.session.query(UserInfo).filter(
                    UserInfo.userID == appUserID
                ).delete(synchronize_session=False)
            else:
                # 第二种情况，用户没有登录过小程序
                # createInfo = {}
                UserInfo.createPublic(createInfo=createInfo)
            db.session.commit()
        except Exception as e:
            return (False, str(e))


#公众号取消关注
#创建用户(公众号）
@app.task
def deleteUser(info):
    wechatManager = WechatManager()
    util = Util()
    openID = info['fromUserName']
    try:
        query = db.session.query(UserInfo).filter(UserInfo.openid1 == openID)
        result = query.first()
        userID = result.userID
        #(1)删除subscribedKey表
        db.session.query(SubscribedKey).filter(
            SubscribedKey.userID == userID
        ).delete(synchronize_session=False)
        #(2)删除searchKey表
        db.session.query(SearchKey).filter(
            SearchKey.foreignID == userID
        ).delete(synchronize_session=False)
        # (3) 删除wechatPush表
        db.session.query(WeChatPush).filter(
            WeChatPush.toUserID == userID
        ).delete(synchronize_session=False)
        # (4) 删除wechatPushHistory表
        db.session.query(WeChatPushHistory).filter(
            WeChatPushHistory.toUserID == userID
        ).delete(synchronize_session=False)
        db.session.commit()
    except Exception as e:
        return (False, str(e))


#创建推送信息
@app.task
def createWeChatPush(info):
    subscribedKeyManager = SubscribedKeyManager()
    return subscribedKeyManager.createWeChatSubscriberList(info=info)


#公众号推送
@app.task
def pushTemplateMessage():
    util = Util()
    (status, accessToken) = util.getAccessToken()
    query = db.session.query(
        WeChatPush, UserInfo, Tender
    ).outerjoin(
        UserInfo, WeChatPush.toUserID == UserInfo.userID
    ).outerjoin(
        Tender, WeChatPush.tenderID == Tender.tenderID
    )
    allResult = query.all()
    postDic = {}
    def generate(result):
        index = len(postDic)
        userInfo = result.UserInfo
        tender = result.Tender
        userID = userInfo.openid1
        templateData = {}
        templateData['touser'] = userID
        templateData['userid'] = userInfo.userID
        templateData['template_id'] = TEMPLATEID
        templateData['url'] = 'http://weixin.qq.com/download'
        templateData['remark'] = '  ' + tender.title + ';' + '\n'
        templateData['miniprogram'] = {
             "appid": MINIAPPID,
             "pagepath":"pages/myFavorite/myFavorite"
        }
        if not postDic.has_key(userID):
            templateData['remark'] = '[1]  ' + templateData['remark']
            postDic[userID] = templateData
            postDic[userID]['count'] = 1
        else:
            postDic[userID]['count'] = postDic[userID]['count'] + 1
            templateData['remark'] = '[' + str(postDic[userID]['count']) + ']  ' + templateData['remark']
            postDic[userID]['remark'] = postDic[userID]['remark'] + templateData['remark']
    [generate(result) for result in allResult]

    for key, value in postDic.iteritems():
        #更新推送历史
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
            WeChatPushHistory.create(createInfo=createInfo)
        pushQuery.delete(synchronize_session=False)
        db.session.commit()
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
        postData = json.dumps(value)
        postUrl = "https://api.weixin.qq.com/cgi-bin/message/template/send?access_token=%s" % accessToken
        urlResp = urllib.urlopen(url=postUrl, data=postData)
        urlResp = json.loads(urlResp.read())
        return (True, urlResp)

