# coding=utf8
import sys
import traceback
import urllib2
import poster
import requests
from sqlalchemy import desc
from tool.tagconfig import USER_TAG_RESPONSIBLEPERSON, PUSH_TENDER_INFO_TAG_STATE_APPROVE, \
    PUSH_TENDER_INFO_TAG_STEP_WAIT
from tool.Util import Util
from tool.config import ErrorInfo

sys.path.append("..")
import os
reload(sys)
sys.setdefaultencoding('utf-8')
import json
from datetime import datetime
from sqlalchemy import func, desc, and_
from tool.tagconfig import USER_TAG_OPERATOR, USER_TAG_RESPONSIBLEPERSON, USER_TAG_AUDITOR, USER_TAG_BOSS
from tool.tagconfig import OPERATOR_TAG_CREATED, DOING_STEP, DONE_STEP, HISTORY_STEP

from models.flask_app import db
from models.PushedTenderInfo import PushedTenderInfo
from models.UserInfo import UserInfo
from models.Tender import Tender
from models.Operator import Operator
from models.Token import Token

from message.MessageManager import MessageManager

class PushedTenderManager(Util):

    def __init__(self):
        pass

    @staticmethod
    def isTokenValidByUserType(info):

        tokenID = info['tokenID']
        util = Util()
        return util.isTokenValid(tokenID=tokenID)
        # userType = info['userType']
        # query = db.session.query(
        #     Token, UserInfo
        # ).outerjoin(
        #     UserInfo, Token.userID == UserInfo.userID
        # ).filter(and_(
        #     UserInfo.userType == userType,
        #     Token.tokenID == tokenID
        # ))
        # result = query.first()
        # if result is None:
        #     errorInfo = ErrorInfo['TENDER_01']
        #     errorInfo['detail'] = result
        #     return (False, errorInfo)
        # token = result.Token
        # now = datetime.now()
        # # 将token登录时间更新为最近的一次操作时间
        # db.session.query(Token).filter(
        #     Token.tokenID == tokenID
        # ).update(
        #     {Token.createTime: now},
        #     synchronize_session=False)
        # try:
        #     db.session.commit()
        # except Exception as e:
        #     print e
        #     errorInfo = ErrorInfo['SPORTS_02']
        #     errorInfo['detail'] = str(e)
        #     db.session.rollback()
        #     return (False, errorInfo)
        # days = (now - token.createTime).days
        # if days > token.validity:
        #     errorInfo = ErrorInfo['SPORTS_01']
        #     errorInfo['detail'] = result
        #     return (False, errorInfo)
        # return (True, result.Token.userID)

    def createMessage(self, info):
        userID = info['userID']
        pushedID = info['pushedID']
        tag = info['tag']
        userResult = db.session.query(UserInfo).filter(
            UserInfo.userID == userID
        ).first()
        if userResult is None:
            return (False, ErrorInfo['TENDER_23'])
        companyID = userResult.customizedCompanyID
        query = db.session.query(UserInfo).filter(
            and_(UserInfo.customizedCompanyID == companyID,
                 UserInfo.userType == tag)
        )
        responResult = query.first()
        if responResult:
            toUserID = responResult.userID
            # 发送消息给负责人
            messageInfo = {}
            messageInfo['fromUserID'] = userID
            messageInfo['pushedID'] = pushedID
            messageInfo['toUserID'] = toUserID
            messageInfo['tag'] = 1
            messageInfo['description'] = ''
            messageInfo['foreignID'] = info['tenderID']
            messageManager = MessageManager()
            return messageManager.createMessage(messageInfo)
        return (False, None)

    # 经办人 负责人 审核人 创建推送
    def createPushedTender(self, info):
        tokenID = info['tokenID']
        (status, userID) = self.isTokenValid(tokenID)
        if status is not True:
            errorInfo = ErrorInfo['TENDER_01']
            return (False, errorInfo)
        pushedID = self.generateID(userID + info['tenderID'])
        info['pushedID'] = pushedID
        info['userID'] = userID
        info['createTime'] = None
        info['responsiblePersonPushedTime'] = None
        info['auditorPushedTime'] = None
        info['state'] = 0
        info['step'] = 0
        tag = info['tag']
        if tag == USER_TAG_OPERATOR:
            info['createTime'] = datetime.now()
        if tag == USER_TAG_AUDITOR:
            info['auditorPushedTime'] = datetime.now()
        if tag == USER_TAG_RESPONSIBLEPERSON:
            info['responsiblePersonPushedTime'] = datetime.now()
        try:
            #判断是否已经创建过推送消息
            result = db.session.query(PushedTenderInfo).filter(
                PushedTenderInfo.tenderID == info['tenderID']
            ).first()
            if result:
                return (False, ErrorInfo['TENDER_25'])
            (status, result) = PushedTenderInfo.create(info)
            #推送消息
            (status, result) = self.createMessage(info=info)
            db.session.commit()
            return (True, pushedID)
        except Exception as e:
            print e
            errorInfo = ErrorInfo['TENDER_02']
            errorInfo['detail'] = str(e)
            db.session.rollback()
            return (False, errorInfo)

    def __generateBrief(self, result):
        res = {}
        res.update(PushedTenderInfo.generateBrief(c=result.PushedTenderInfo))
        res.update(Tender.generateBrief(tender=result.Tender))
        return res

    def __generateUndistributedBrief(self, result):
        res = {}
        res.update(PushedTenderInfo.generateBrief(c=result.PushedTenderInfo))
        res.update(Tender.generateBrief(tender=result.Tender))
        if result.Operator:
            query = db.session.query(UserInfo).filter(UserInfo.userID == result.Operator.userID)
            userInfo = query.first()
            res.update(UserInfo.generateBrief(userInfo))
            res.update(Operator.generate(c=result.Operator))
        else:
            res.update({'state': -1,
                        'userName': '',
                        'userID': ''})
        return res

    # 负责人或审核人推送, 从上一级或上两级中继续推送
    def updatePushedTenderInfo(self, info):
        pushedID = info['pushedID']
        userType = info['userType']
        state = int(info['state'])
        try:
            query = db.session.query(PushedTenderInfo).filter(
                PushedTenderInfo.pushedID == pushedID
            )
            result = query.first()
            tenderID = result.tenderID
            if not result:
                return (False, ErrorInfo['TENDER_25'])
            updateInfo = {}
            if userType == USER_TAG_AUDITOR:
                updateInfo = {
                    PushedTenderInfo.auditorPushedTime : datetime.now()
                }
            elif userType == USER_TAG_RESPONSIBLEPERSON:
                updateInfo = {
                    PushedTenderInfo.responsiblePersonPushedTime : datetime.now()
                }
            elif userType == USER_TAG_BOSS:
                updateInfo = {
                    PushedTenderInfo.state : state
                }
            query.update(
                updateInfo, synchronize_session=False
            )
            #如果同意投标，创建一个默认的经办人
            if state == 1:
                operatorInfo = {}
                operatorInfo['operatorID'] = self.generateID(tenderID)
                operatorInfo['tenderID'] = tenderID
                operatorInfo['userID'] = -1
                operatorInfo['state'] = 0
                Operator.create(info=operatorInfo)
            db.session.commit()
            return (True, None)
        except Exception as e:
            print e
            errorInfo = ErrorInfo['TENDER_02']
            errorInfo['detail'] = str(e)
            db.session.rollback()
            return (False, errorInfo)


    # 经办人 获取我的推送列表, 其他人获取经办人推送列表
    def getPushedTenderListByUserID(self, info):
        startIndex = info['startIndex']
        pageCount = info['pageCount']
        userID = info['userID']

        try:
            query = db.session.query(
                PushedTenderInfo, Tender
            ).outerjoin(
                Tender, PushedTenderInfo.tenderID == Tender.tenderID
            ).filter(
                PushedTenderInfo.userID == userID
            )
            countQuery = db.session.query(func.count(PushedTenderInfo.pushedID)).filter(
                PushedTenderInfo.userID == userID
            )
            count = countQuery.first()
            count = count[0]
            allResult = query.offset(startIndex).limit(pageCount).all()
            dataList = [self.__generateBrief(result=result) for result in allResult]
            callBackInfo = {}
            callBackInfo['dataList'] = dataList
            callBackInfo['count'] = count
            return (True, callBackInfo)
        except Exception as e:
            print e
            errorInfo = ErrorInfo['TENDER_02']
            errorInfo['detail'] = str(e)
            db.session.rollback()
            return (False, errorInfo)

    # 获取正在进行中的列表
    def __getTenderDoingList(self, info):
        tokenID = info['tokenID']
        startIndex = info['startIndex']
        pageCount = info['pageCount']
        step = info['step']
        (status, logInUserID) = self.isTokenValid(tokenID)
        if status is not True:
            errorInfo = ErrorInfo['TENDER_01']
            return (False, errorInfo)
        if info.has_key('userID'):
            userID = info['userID']
        else:
            userID = logInUserID
        try:
            query = db.session.query(
                PushedTenderInfo, Tender
            ).outerjoin(
                Tender, PushedTenderInfo.tenderID == Tender.tenderID
            ).filter(
                and_(PushedTenderInfo.userID == userID,
                     PushedTenderInfo.step == step)
            )
            countQuery = db.session.query(func.count(PushedTenderInfo.pushedID)).filter(
                and_(PushedTenderInfo.userID == userID,
                     PushedTenderInfo.step == step)
            )
            count = countQuery.first()
            count = count[0]
            allResult = query.offset(startIndex).limit(pageCount).all()
            dataList = [self.__generateBrief(result=result) for result in allResult]
            callBackInfo = {}
            callBackInfo['dataList'] = dataList
            callBackInfo['count'] = count
            return (True, callBackInfo)
        except Exception as e:
            print e
            errorInfo = ErrorInfo['TENDER_02']
            errorInfo['detail'] = str(e)
            db.session.rollback()
            return (False, errorInfo)

    def __getAllTenderDoingList(self, info):
        tokenID = info['tokenID']
        startIndex = info['startIndex']
        pageCount = info['pageCount']
        step = info['step']
        try:
            query = db.session.query(
                PushedTenderInfo, Tender
            ).outerjoin(
                Tender, PushedTenderInfo.tenderID == Tender.tenderID
            ).filter(PushedTenderInfo.step == step)
            countQuery = db.session.query(
                func.count(PushedTenderInfo.pushedID)
            ).filter(PushedTenderInfo.step == step)
            count = countQuery.first()
            count = count[0]
            allResult = query.offset(startIndex).limit(pageCount).all()
            dataList = [self.__generateBrief(result=result) for result in allResult]
            callBackInfo = {}
            callBackInfo['dataList'] = dataList
            callBackInfo['count'] = count
            return (True, callBackInfo)
        except Exception as e:
            print e
            errorInfo = ErrorInfo['TENDER_02']
            errorInfo['detail'] = str(e)
            db.session.rollback()
            return (False, errorInfo)

    # 审核人 负责人 获取我的推送
    def getPushedTenderListByUserType(self, info):
        startIndex = info['startIndex']
        pageCount = info['pageCount']
        userType = info['userType']

        try:
            query = db.session.query(
                PushedTenderInfo, Tender
            ).outerjoin(
                Tender, PushedTenderInfo.tenderID == Tender.tenderID
            )
            countQuery = db.session.query(
                func.count(PushedTenderInfo.pushedID)
            )
            # 负责人查询
            if userType == USER_TAG_RESPONSIBLEPERSON:
                query = query.filter(
                    PushedTenderInfo.responsiblePersonPushedTime != None
                ).order_by(desc(
                    PushedTenderInfo.responsiblePersonPushedTime
                ))
                countQuery = countQuery.filter(
                    PushedTenderInfo.responsiblePersonPushedTime != None
                )
            #     审核人查询
            elif userType == USER_TAG_AUDITOR:
                query = query.filter(
                    PushedTenderInfo.auditorPushedTime != None
                ).order_by(desc(
                    PushedTenderInfo.auditorPushedTime
                ))
                countQuery = countQuery.filter(
                    PushedTenderInfo.auditorPushedTime != None
                )
            allResult = query.offset(startIndex).limit(pageCount).all()
            count = countQuery.first()
            dataList = [self.__generateBrief(result=result) for result in allResult]
            callBackInfo = {}
            callBackInfo['dataList'] = dataList
            callBackInfo['count'] = count[0]
            return (True, callBackInfo)
        except Exception as e:

            print e
            errorInfo = ErrorInfo['TENDER_02']
            errorInfo['detail'] = str(e)
            db.session.rollback()
            return (False, errorInfo)

    # boss是否指定该经办人
    def validateOperator(self, info):
        tenderID = info['tenderID']
        state = info['state']
        try:
            query = db.session.query(Operator).filter(
                and_(Operator.tenderID == tenderID,
                     Operator.state == 0)
            )
            result = query.first()
            if result:
                updateInfo = {
                    Operator.state: int(state)
                }
                query.update(
                    updateInfo, synchronize_session=False
                )
                db.session.commit()
                return (True, None)
            else:
                return (False, ErrorInfo['TENDER_26'])
        except Exception as e:
            print e
            errorInfo = ErrorInfo['TENDER_02']
            errorInfo['detail'] = str(e)
            db.session.rollback()
            return (False, errorInfo)


    def getUndistributedTenderList(self, info):
        startIndex = info['startIndex']
        pageCount = info['pageCount']
        try:
            query = db.session.query(
                PushedTenderInfo, Tender, Operator
            ).outerjoin(
                Tender, PushedTenderInfo.tenderID == Tender.tenderID
            ).outerjoin(
                Operator, PushedTenderInfo.tenderID == Operator.tenderID
            ).filter(and_(
                PushedTenderInfo.state == PUSH_TENDER_INFO_TAG_STATE_APPROVE,
                PushedTenderInfo.step == PUSH_TENDER_INFO_TAG_STEP_WAIT
            ))
            countQuery = db.session.query(func.count(PushedTenderInfo.pushedID)).filter(and_(
                PushedTenderInfo.state == PUSH_TENDER_INFO_TAG_STATE_APPROVE,
                PushedTenderInfo.step == PUSH_TENDER_INFO_TAG_STEP_WAIT
            ))
            count = countQuery.first()
            count = count[0]
            allResult = query.offset(startIndex).limit(pageCount).all()
            dataList = [self.__generateUndistributedBrief(result=result) for result in allResult]
            callBackInfo = {}
            callBackInfo['dataList'] = dataList
            callBackInfo['count'] = count
            return (True, callBackInfo)
        except Exception as e:
            print e
            errorInfo = ErrorInfo['TENDER_02']
            errorInfo['detail'] = str(e)
            db.session.rollback()
            return (False, errorInfo)

    def getDistributedTenderList(self, info):
        startIndex = info['startIndex']
        pageCount = info['pageCount']
        try:
            query = db.session.query(
                PushedTenderInfo, Tender, Operator
            ).outerjoin(
                Tender, PushedTenderInfo.tenderID == Tender.tenderID
            ).outerjoin(
                Operator, PushedTenderInfo.tenderID == Operator.tenderID
            ).filter(and_(
                PushedTenderInfo.state == PUSH_TENDER_INFO_TAG_STATE_APPROVE,
                PushedTenderInfo.step == PUSH_TENDER_INFO_TAG_STEP_WAIT
            ))
            countQuery = db.session.query(func.count(PushedTenderInfo.pushedID)).filter(and_(
                PushedTenderInfo.state == PUSH_TENDER_INFO_TAG_STATE_APPROVE,
                PushedTenderInfo.step == PUSH_TENDER_INFO_TAG_STEP_WAIT
            ))
            count = countQuery.first()
            count = count[0]
            allResult = query.offset(startIndex).limit(pageCount).all()
            dataList = [self.__generateUndistributedBrief(result=result) for result in allResult]
            callBackInfo = {}
            callBackInfo['dataList'] = dataList
            callBackInfo['count'] = count
            return (True, callBackInfo)
        except Exception as e:
            print e
            errorInfo = ErrorInfo['TENDER_02']
            errorInfo['detail'] = str(e)
            db.session.rollback()
            return (False, errorInfo)

    # 经办人特殊, 获取自己参与的, 正在进行中的列表
    # 考虑策略模式

    def getTenderDoingList(self, jsonInfo):
        info = json.loads(jsonInfo)
        userType = info['userType']
        (status, userID) = self.isTokenValidByUserType(info=info)
        if status is not True:
            errorInfo = ErrorInfo['TENDER_01']
            return (False, errorInfo)
        info['step'] = DOING_STEP
        if userType == USER_TAG_OPERATOR:
            return self.__getTenderDoingList(info=info)
        else:
            return self.__getAllTenderDoingList(info=info)

    def getTenderDoingDetail(self, jsonInfo):
        pass

        # 经办人特殊, 获取自己参与的, 已完成的列表

    def getTenderDoneList(self, jsonInfo):
        info = json.loads(jsonInfo)
        userType = info['userType']
        (status, userID) = self.isTokenValidByUserType(info=info)
        if status is not True:
            errorInfo = ErrorInfo['TENDER_01']
            return (False, errorInfo)
        info['step'] = DOING_STEP
        if userType == USER_TAG_OPERATOR:
            return self.__getTenderDoingList(info=info)
        else:
            return self.__getAllTenderDoingList(info=info)

    def getTenderDoneDetail(self, jsonInfo):
        pass

        # 经办人特殊, 获取自己参与的, 历史记录

    def getTenderHistoryList(self, jsonInfo):
        info = json.loads(jsonInfo)
        userType = info['userType']
        (status, userID) = self.isTokenValidByUserType(info=info)
        if status is not True:
            errorInfo = ErrorInfo['TENDER_01']
            return (False, errorInfo)
        info['step'] = DOING_STEP
        if userType == USER_TAG_OPERATOR:
            return self.__getTenderDoingList(info=info)
        else:
            return self.__getAllTenderDoingList(info=info)

    def getTenderHistoryDetail(self, jsonInfo):
        pass
