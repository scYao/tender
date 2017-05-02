#coding: utf-8

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
from models.Favorite import Favorite
from models.Token import Token
from models.flask_app import db
from wechatPublic.WechatManager import WechatManager
from tool.Util import Util

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
                db.session.query(Tender).filter(
                    Tender.userID == appUserID
                ).update({Token.userID: userID}, synchronize_session=False)
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
                #(5)删除userInfo中的appUserID
                db.session.query(UserInfo).filter(
                    UserInfo.userID == appUserID
                ).delete(synchronize_session=False)
            else:
                # 第二种情况，用户没有登录过小程序
                createInfo = {}
                UserInfo.createPublic(createInfo=createInfo)
            db.session.commit()
        except Exception, Argument:
            return (False, Argument)


