# coding=utf8
import sys
import urllib2
import poster
import requests
import json
import re


sys.path.append("..")
import os
reload(sys)
sys.setdefaultencoding('utf-8')
from tool.config import ErrorInfo
from user.AdminManager import AdminManager

from datetime import datetime
from sqlalchemy import or_, desc, func
from tool.Util import Util
from models.flask_app import db, cache
from models.Message import Message


class MessageManager(Util):

    def __init__(self):
        pass

    ##融云推送消息列表，后台管理
    # def getPushedRYMessageListBackground(self, jsonInfo):
    #     info = json.loads(jsonInfo)
    #     startIndex = info['startIndex']
    #     pageCount = info['pageCount']
    #     searchKey = info['searchKey']
    #     #验证管理员信息
    #     adminManager = AdminManager()
    #     (status, adminID) = adminManager.adminAuth(jsonInfo)
    #     if status is not True:
    #         return (False, adminID)
    #
    #     messageQuery = db.session.query(PushedRYMessage)
    #
    #     if searchKey != '-1':
    #         messageQuery = messageQuery.filter(or_(
    #             PushedRYMessage.description.ilike('%%%s%%' % searchKey),
    #             PushedRYMessage.remark.ilike('%%%s%%' % searchKey)
    #         ))
    #
    #     allResult = messageQuery.group_by(PushedRYMessage.tag).order_by(
    #         desc(PushedRYMessage.createTime)
    #     ).offset(startIndex).limit(pageCount).all()
    #
    #     # UserInfo信息
    #     def generateMessageInfo(result):
    #         pushedRYMessageInfo = {}
    #         pushedRYMessageInfo['messageID'] = result.messageID
    #         pushedRYMessageInfo['description'] = result.description
    #         pushedRYMessageInfo['createTime'] = str(result.createTime)
    #         pushedRYMessageInfo['userID'] = result.userID
    #         pushedRYMessageInfo['remark'] = result.remark
    #         return pushedRYMessageInfo
    #
    #     pushedRYMessageInfoList = [generateMessageInfo(result) for result in allResult]
    #
    #     return (True, pushedRYMessageInfoList)

    #创建融云消息，后台管理
    # def pushRYMessageToAllUsersBackground(self, jsonInfo):
    #     info = json.loads(jsonInfo)
    #     description = info['description'].replace('\'', '\\\'').replace('\"', '\\\"')
    #     remark = info['remark']
    #     # 这是一个字符串,不是列表
    #     telDList = info['telList']
    #     fromUserID = OFFICIAL_USER_ID
    #     # 验证管理员信息
    #     adminManager = AdminManager()
    #     (status, adminID) = adminManager.adminAuth(jsonInfo)
    #     if status is not True:
    #         return (False, adminID)
    #     createtime = datetime.now()
    #     #获取发送消息用户列表
    #     allQuery = db.session.query(UserInfo).filter(
    #         UserInfo.tel != None
    #     )
    #     if telDList != '-1':
    #         telList = re.split('\W+', telDList)
    #         telTuple = tuple(telList)
    #         allQuery = allQuery.filter(
    #             UserInfo.tel.in_(telTuple)
    #         )
    #
    #     allResult = allQuery.all()
    #
    #
    #     # UserInfo信息
    #     tag = self.generateID(description)
    #     ryClient = RYClient()
    #
    #     def generateMessageInfo(result):
    #         toUserID = result.userID
    #         messageID = self.generateID(toUserID)
    #         #发送融云消息
    #         #创建消息记录
    #         pushedRYMessage = PushedRYMessage(messageID=messageID, description=description,
    #                                           createTime=createtime, userID=toUserID,
    #                                           remark=remark, tag=tag)
    #         db.session.add(pushedRYMessage)
    #         return toUserID
    #     toUserIDList = [generateMessageInfo(result) for result in allResult]
    #     length = 100
    #     bufferUserIDList = [toUserIDList[i:i+length] for i in xrange(0, len(toUserIDList), length)]
    #     for uList in bufferUserIDList:
    #         code = ryClient.publishMessage(fromUserID, uList, description)
    #         if code != 200:
    #             errorInfo = ErrorInfo['SPORTS_32']
    #             errorInfo['detail'] = code
    #             return (False, errorInfo)
    #     try:
    #         db.session.commit()
    #     except Exception as e:
    #         print e
    #         errorInfo = ErrorInfo['SPORTS_02']
    #         errorInfo['detail'] = str(e)
    #         db.session.rollback()
    #         return (False, errorInfo)
    #     return (True, None)

    ############################
    ### 以下接口为未读消息接口  ###
    ############################

    # 创建未读消息
    def createMessage(self, info):
        foreignID = info['foreignID']
        description = info['description'].replace('\'', '\\\'').replace('\"', '\\\"')
        # 用以区分消息类型 1 代表钱包消息， 2代表收藏消息， 3代表买家评论消息， 4代表邀请码消息
        tag = info['tag']
        # 以下三个参数只有评论消息才有, 否则为'-1'
        fromUserID = info['fromUserID']
        toUserID = info['toUserID']

        messageID = self.generateID(foreignID + description)
        message = Message(messageID=messageID, foreignID=foreignID,
                          fromUserID=fromUserID, toUserID=toUserID,
                          description=description, tag=tag)
        db.session.add(message)
        return (True, messageID)

    #  删除未读消息
    def deleteMessages(self, jsonInfo):
        info = json.loads(jsonInfo)
        messageIDList = info['messageIDList']
        messageIDTuple = tuple(messageIDList)
        try:
            db.session.query(Message).filter(
                Message.messageID.in_(messageIDTuple)
            ).delete(synchronize_session=False)
        except Exception as e:
            print str(e)
            # traceback.print_stack()
            db.session.rollback()
            errorInfo = ErrorInfo['TENDER_02']
            errorInfo['detail'] = str(e)
            return (False, errorInfo)
        return (True, None)

    # 获取未读消息列表
    def getMessageList(self, jsonInfo):
        info = json.loads(jsonInfo)
        userID = info['userID']
        allResult = db.session.query(Message).filter(
            Message.toUserID == userID
        ).order_by(desc(Message.createTime)).all()

        messageList = [Message.generate(o=o) for o in allResult]
        try:
            count = db.session.query(func.count(Message.messageID)).filter(
                Message.toUserID == userID
            ).first()
        except Exception as e:
            print str(e)
            # traceback.print_stack()
            db.session.rollback()
            errorInfo = ErrorInfo['TENDER_02']
            errorInfo['detail'] = str(e)
            return (False, errorInfo)
        result = {}
        result['messageList'] = messageList
        result['count'] = count[0]

        return (True, result)
