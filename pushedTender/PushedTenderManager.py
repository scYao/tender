# coding=utf8
import sys
import traceback
import urllib2
import poster
import requests
from sqlalchemy import desc
from tool.tagconfig import USER_TAG_RESPONSIBLEPERSON, PUSH_TENDER_INFO_TAG_STATE_APPROVE, \
    PUSH_TENDER_INFO_TAG_STEP_WAIT, PUSH_TENDER_INFO_TAG_STEP_DOING, OPERATOR_TAG_YES
from tool.Util import Util
from tool.config import ErrorInfo

sys.path.append("..")
import os
reload(sys)
sys.setdefaultencoding('utf-8')
import json
from datetime import datetime
from sqlalchemy import func, desc, and_, or_
from tool.tagconfig import USER_TAG_OPERATOR, USER_TAG_RESPONSIBLEPERSON, USER_TAG_AUDITOR, USER_TAG_BOSS
from tool.tagconfig import OPERATOR_TAG_CREATED, DOING_STEP, DONE_STEP, HISTORY_STEP

from models.flask_app import db
from models.PushedTenderInfo import PushedTenderInfo
from models.UserInfo import UserInfo
from models.Tender import Tender
from models.Operator import Operator
from models.Token import Token
from models.City import City

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
        res.update(Operator.generate(c=result.Operator))
        return res

    def __generateUndistributedBrief(self, result):
        res = {}
        res.update(PushedTenderInfo.generateBrief(c=result.PushedTenderInfo))
        res.update(Tender.generateBrief(tender=result.Tender))
        res.update(Operator.generate(c=result.Operator))
        # if result.Operator:
        #     query = db.session.query(UserInfo).filter(UserInfo.userID == result.Operator.userID)
        #     userInfo = query.first()
        #     res.update(UserInfo.generateBrief(userInfo))
        #     res.update(Operator.generate(c=result.Operator))
        # else:
        #     res.update({'state': -1,
        #                 'userName': '',
        #                 'userID': ''})
        return res

    # 负责人或审核人推送, 从上一级或上两级中继续推送
    def updatePushedTenderInfo(self, info):
        pushedID = info['pushedID']
        userType = info['userType']

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
                state = int(info['state'])
                updateInfo = {
                    PushedTenderInfo.state : state
                }
                #如果同意投标，创建一个默认的经办人
                if state == 1:
                    operatorInfo = {}
                    operatorInfo['operatorID'] = self.generateID(tenderID)
                    operatorInfo['tenderID'] = tenderID
                    operatorInfo['userID'] = -1
                    operatorInfo['state'] = 0
                    Operator.create(info=operatorInfo)
            query.update(
                updateInfo, synchronize_session=False
            )

            db.session.commit()
            return (True, None)
        except Exception as e:
            print e
            errorInfo = ErrorInfo['TENDER_02']
            errorInfo['detail'] = str(e)
            db.session.rollback()
            return (False, errorInfo)

    def __generatePushedBrief(self, result):
        res = {}
        res.update(PushedTenderInfo.generateBrief(c=result.PushedTenderInfo))
        res.update(Tender.generateBrief(tender=result.Tender))
        return res

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
            dataList = [self.__generatePushedBrief(result=result) for result in allResult]
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
                PushedTenderInfo, Tender, Operator
            ).outerjoin(
                Operator, PushedTenderInfo.tenderID == Operator.tenderID
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
            userIDTuple = (o.Operator.userID for o in allResult)
            cityIDTuple = (o.Tender.cityID for o in allResult)
            userQuery = db.session.query(UserInfo).filter(
                UserInfo.userID.in_(userIDTuple)
            )
            cityQuery = db.session.query(City).filter(
                City.cityID.in_(cityIDTuple)
            )
            userResult = userQuery.all()
            cityResult = cityQuery.all()
            userDic = {}
            cityDic = {}
            for o in userResult:
                userDic[o.userID] = o.userName
            for o in cityResult:
                cityDic[o.cityID] = o.cityName
            dataList = [self.__generateBrief(result=result) for result in allResult]
            for o in dataList:
                o['cityName'] = cityDic[o['cityID']]
                if o['userID'] != '-1':
                    o['userName'] = userDic[o['userID']]
                else:
                    o['userName'] = ''
            callBackInfo = {}
            callBackInfo['dataList'] = dataList
            callBackInfo['count'] = count
            return (True, callBackInfo)
        except Exception as e:
            print e
            traceback.print_exc()
            errorInfo = ErrorInfo['TENDER_02']
            errorInfo['detail'] = str(e)
            db.session.rollback()
            return (False, errorInfo)

    def __getAllTenderDoingList(self, info):
        startIndex = info['startIndex']
        pageCount = info['pageCount']
        step = info['step']
        try:
            query = db.session.query(
                PushedTenderInfo, Tender, Operator
            ).outerjoin(
                Tender, PushedTenderInfo.tenderID == Tender.tenderID
            ).outerjoin(
                Operator, PushedTenderInfo.tenderID == Operator.tenderID
            ).filter(PushedTenderInfo.step == step)
            countQuery = db.session.query(
                func.count(PushedTenderInfo.pushedID)
            ).filter(PushedTenderInfo.step == step)
            count = countQuery.first()
            count = count[0]
            allResult = query.offset(startIndex).limit(pageCount).all()
            userIDTuple = (o.Operator.userID for o in allResult if o.Operator)
            cityIDTuple = (o.Tender.cityID for o in allResult)
            userQuery = db.session.query(UserInfo).filter(
                UserInfo.userID.in_(userIDTuple)
            )
            cityQuery = db.session.query(City).filter(
                City.cityID.in_(cityIDTuple)
            )
            userResult = userQuery.all()
            cityResult = cityQuery.all()
            userDic = {}
            cityDic = {}
            for o in userResult:
                userDic[o.userID] = o.userName
            for o in cityResult:
                cityDic[o.cityID] = o.cityName
            dataList = [self.__generateBrief(result=result) for result in allResult]
            for o in dataList:
                o['cityName'] = cityDic[o['cityID']]
                if o['userID'] != '-1':
                    o['userName'] = userDic[o['userID']]
                else:
                    o['userName'] = ''
            callBackInfo = {}
            callBackInfo['dataList'] = dataList
            callBackInfo['count'] = count
            return (True, callBackInfo)
        except Exception as e:
            print e
            traceback.print_exc()
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
            dataList = [self.__generatePushedBrief(result=result) for result in allResult]
            callBackInfo = {}
            callBackInfo['dataList'] = dataList
            callBackInfo['count'] = count[0]
            return (True, callBackInfo)
        except Exception as e:
            traceback.print_exc()
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
            # 先将经办人的状态改为同意或驳回
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
                if state == OPERATOR_TAG_YES:
                    pushedQuery = db.session.query(PushedTenderInfo).filter(
                        PushedTenderInfo.tenderID == tenderID
                    )
                    pushedQuery.update({
                        PushedTenderInfo.step : PUSH_TENDER_INFO_TAG_STEP_DOING
                    }, synchronize_session=False)
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
            # 获取所有已同意投标，并且状态时未开始的标段
            query = db.session.query(
                PushedTenderInfo, Operator, Tender
            ).outerjoin(
                Operator, PushedTenderInfo.tenderID == Operator.tenderID
            ).outerjoin(
                Tender, PushedTenderInfo.tenderID == Tender.tenderID
            ).filter(and_(
                PushedTenderInfo.state == PUSH_TENDER_INFO_TAG_STATE_APPROVE,
                PushedTenderInfo.step == PUSH_TENDER_INFO_TAG_STEP_WAIT,
                or_(Operator.userID == '-1',
                    Operator.state == 2)
            ))

            pushedInfoResult = query.offset(startIndex).limit(pageCount).all()
            userIDTuple = (o.Operator.userID for o in pushedInfoResult)

            userQuery = db.session.query(UserInfo).filter(
                UserInfo.userID.in_(userIDTuple)
            )
            userResult = userQuery.all()
            userDic = {}
            for o in userResult:
                userDic[o.userID] = o.userName

            resultList = [self.__generateUndistributedBrief(result=o) for o in pushedInfoResult]
            for o in resultList:
                if o['userID'] != '-1':
                    o['userName'] = userDic[o['userID']]
                else:
                    o['userName'] = ''

            countQuery = db.session.query(func.count(PushedTenderInfo.tenderID), Operator).outerjoin(
                Operator, PushedTenderInfo.tenderID == Operator.tenderID
            ).filter(and_(
                PushedTenderInfo.state == PUSH_TENDER_INFO_TAG_STATE_APPROVE,
                PushedTenderInfo.step == PUSH_TENDER_INFO_TAG_STEP_WAIT,
                or_(Operator.userID == '-1',
                    Operator.state == 2)
            ))
            count = countQuery.first()
            callBackInfo = {}
            callBackInfo['dataList'] = resultList
            callBackInfo['count'] = count[0]
            return (True, callBackInfo)

        except Exception as e:
            print e
            traceback.print_exc()
            errorInfo = ErrorInfo['TENDER_02']
            errorInfo['detail'] = str(e)
            db.session.rollback()
            return (False, errorInfo)

    def getDistributedTenderList(self, info):
        startIndex = info['startIndex']
        pageCount = info['pageCount']
        query = db.session.query(
            PushedTenderInfo, Operator, Tender
        ).outerjoin(
            Operator, PushedTenderInfo.tenderID == Operator.tenderID
        ).outerjoin(
            Tender, PushedTenderInfo.tenderID == Tender.tenderID
        ).filter(and_(
            PushedTenderInfo.state == PUSH_TENDER_INFO_TAG_STATE_APPROVE,
            PushedTenderInfo.step == PUSH_TENDER_INFO_TAG_STEP_WAIT,
            Operator.userID != '-1',
            Operator.state == 0
        ))

        pushedInfoResult = query.offset(startIndex).limit(pageCount).all()
        userIDTuple = (o.Operator.userID for o in pushedInfoResult)

        userQuery = db.session.query(UserInfo).filter(
            UserInfo.userID.in_(userIDTuple)
        )
        userResult = userQuery.all()
        userDic = {}
        for o in userResult:
            userDic[o.userID] = o.userName

        resultList = [self.__generateUndistributedBrief(result=o) for o in pushedInfoResult]
        for o in resultList:
            if o['userID'] != '-1':
                o['userName'] = userDic[o['userID']]
            else:
                o['userName'] = ''

        countQuery = db.session.query(PushedTenderInfo).filter(and_(
                PushedTenderInfo.state == PUSH_TENDER_INFO_TAG_STATE_APPROVE,
                PushedTenderInfo.step == PUSH_TENDER_INFO_TAG_STEP_WAIT,
                or_(Operator.userID != '-1',
                        Operator.state == 0)
                ))
        countResult = countQuery.all()
        countPushedIDTuple = (o.tenderID for o in countResult)
        countQuery = db.session.query(func.count(Operator.operatorID)).filter(
            and_(Operator.tenderID.in_(countPushedIDTuple),
                or_(Operator.userID != '-1',
                    Operator.state == 0))
        )
        count = countQuery.first()
        callBackInfo = {}
        callBackInfo['dataList'] = resultList
        callBackInfo['count'] = count[0]
        return (True, callBackInfo)

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
