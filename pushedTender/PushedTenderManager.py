# coding=utf8
import sys
import traceback
import urllib2
import poster
import requests
from sqlalchemy import desc
from tool.tagconfig import USER_TAG_RESPONSIBLEPERSON, PUSH_TENDER_INFO_TAG_STATE_APPROVE, \
    PUSH_TENDER_INFO_TAG_STEP_WAIT, PUSH_TENDER_INFO_TAG_STEP_DOING, OPERATOR_TAG_YES, OPERATION_TAG_TENDER_PLAN, \
    OPERATION_TAG_TENDER_PRICE, OPERATION_TAG_DEPOSIT, OPERATION_TAG_MAKE_BIDDING_BOOK, BID_DOC_DIRECTORY, \
    CUS_TENDER_DOC_DIRECTORY, OPERATION_TAG_MANAGER_ARRANGEMENT, PUSH_TENDER_INFO_TAG_STATE_DISCARD, \
    PUSH_TENDER_INFO_TAG_STATE_UNREAD
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
from tool.tagconfig import  MESSAGE_PUSH_DIC, MESSAGE_ASSIGN_DIC

from models.flask_app import db
from models.PushedTenderInfo import PushedTenderInfo
from models.UserInfo import UserInfo
from models.Tender import Tender
from models.CustomizedTender import CustomizedTender
from models.Operator import Operator
from models.Token import Token
from models.City import City
from models.QuotedPrice import QuotedPrice
from models.Operation import Operation
from models.ImgPath import ImgPath
from models.TenderComment import TenderComment

from message.MessageManager import MessageManager
from user.UserManager import UserManager

class PushedTenderManager(Util):

    def __init__(self):
        self.resp = None

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

    def createPushMessage(self, info):
        tag = info['tag']
        pushedID = info['pushedID']
        messageManager = MessageManager()
        toUserQuery = db.session.query(UserInfo).filter(
            UserInfo.userType == MESSAGE_PUSH_DIC[tag]
        )
        toUserResult = toUserQuery.first()
        if toUserResult:
            info['toUserID'] = toUserResult.userID
            info['description'] = MESSAGE_PUSH_DIC['description']
            info['messageTag'] = MESSAGE_PUSH_DIC['tag']
            info['foreignID'] = pushedID
            (status, result) = messageManager.createOAMessage(info=info)
            return (True, None)
        else:
            return (False, None)


    # 经办人 负责人 审核人 创建推送
    def createPushedTender(self, info):
        userID = info['userID']
        tenderID = info['tenderID']
        pushedID = self.generateID(userID + tenderID)
        info['pushedID'] = pushedID
        info['userID'] = userID
        info['operatorPersonPushedTime'] = None
        info['responsiblePersonPushedTime'] = None
        info['auditorPushedTime'] = None
        info['state'] = 0
        info['step'] = 0
        info['createTime'] = datetime.now()
        if not info.has_key('deadline'):
            info['deadline'] = None
        userType = info['userType']
        if userType == USER_TAG_OPERATOR:
            info['operatorPersonPushedTime'] = datetime.now()
        if userType == USER_TAG_AUDITOR:
            info['auditorPushedTime'] = datetime.now()
        if userType == USER_TAG_RESPONSIBLEPERSON:
            info['responsiblePersonPushedTime'] = datetime.now()
        #推送人是审定人，直接视为推送到审定人且审定人决定投标,分配一个默认的经办人
        if userType == USER_TAG_BOSS:
            info['state'] = 1
        try:
            #判断是否已经创建过推送消息
            result = db.session.query(PushedTenderInfo).filter(
                PushedTenderInfo.tenderID == tenderID
            ).first()
            if result:
                return (False, ErrorInfo['TENDER_25'])
            (status, result) = PushedTenderInfo.create(info)
            db.session.commit()
            if status is True and userType == USER_TAG_BOSS:
                operatorInfo = {}
                operatorInfo['operatorID'] = self.generateID(tenderID)
                operatorInfo['tenderID'] = tenderID
                operatorInfo['userID'] = -1
                operatorInfo['state'] = 0
                Operator.create(info=operatorInfo)
                self.createAssignMessage(info=info)
                db.session.commit()
            return (True, pushedID)
        except Exception as e:
            print e
            traceback.print_stack()
            errorInfo = ErrorInfo['TENDER_02']
            errorInfo['detail'] = str(e)
            db.session.rollback()
            return (False, errorInfo)

    # 经办人 负责人 审核人 审定人撤销推送
    def deletePushedTender(self, info):
        pushedID = info['pushedID']
        userType = info['userType']
        try:
            query = db.session.query(PushedTenderInfo).filter(
                    PushedTenderInfo.pushedID == pushedID
            )
            result = query.first()
            if result is None:
                return (False, ErrorInfo['TENDER_28'])#推送消息不存在
            operatorPersonPushedTime = result.operatorPersonPushedTime
            responsiblePersonPushedTime = result.responsiblePersonPushedTime
            auditorPushedTime = result.auditorPushedTime
            state = result.state

            #(1)判断取消人身份，（２）判断是否可以取消，（３）根据不同身份返回到推送前状态
            if userType == USER_TAG_OPERATOR:
                if state != PUSH_TENDER_INFO_TAG_STATE_UNREAD or \
                                responsiblePersonPushedTime is not None or \
                                auditorPushedTime is not None:
                    return (False, ErrorInfo['TENDER_35'])
                query.delete(synchronize_session=False)

            if userType == USER_TAG_RESPONSIBLEPERSON:
                if state != PUSH_TENDER_INFO_TAG_STATE_UNREAD or \
                             auditorPushedTime is not None:
                    return (False, ErrorInfo['TENDER_35'])
                else:
                    if operatorPersonPushedTime is not None:
                        query.update(
                            {PushedTenderInfo.responsiblePersonPushedTime: None},
                            synchronize_session=False
                        )
                    else:
                        query.delete(synchronize_session=False)

            if userType == USER_TAG_AUDITOR:
                if state != PUSH_TENDER_INFO_TAG_STATE_UNREAD:
                    return (False, ErrorInfo['TENDER_35'])
                else:
                    if responsiblePersonPushedTime is not None:
                        query.update(
                            {PushedTenderInfo.auditorPushedTime: None},
                            synchronize_session=False
                        )
                    else:
                        query.delete(synchronize_session=False)
            db.session.commit()
            return (True, None)
        except Exception as e:
            print e
            traceback.print_stack()
            errorInfo = ErrorInfo['TENDER_02']
            errorInfo['detail'] = str(e)
            db.session.rollback()
            return (False, errorInfo)


    # 添加项目信息，正在进行中
    def updateDoingPushedTender(self, info):
        userID = info['userID']
        tenderID = info['tenderID']
        query = db.session.query(Operator).filter(
            Operator.tenderID == tenderID
        )
        result = query.first()
        if result.userID != userID:
            return (False, ErrorInfo['TENDER_27'])#不是经办人，无法填写
        try:
            query = db.session.query(PushedTenderInfo).filter(
                PushedTenderInfo.tenderID == tenderID
            )
            result = query.first()
            if result:
                updateInfo = {
                    PushedTenderInfo.projectManagerName: info['projectManagerName'],
                    PushedTenderInfo.openedDate: info['openedDate'],
                    PushedTenderInfo.openedLocation: info['openedLocation'],
                    PushedTenderInfo.ceilPrice: info['ceilPrice'],
                    PushedTenderInfo.tenderInfoDescription: info['tenderInfoDescription'],
                    PushedTenderInfo.tenderCompanyName: info['tenderCompanyName'],
                    PushedTenderInfo.projectType: info['projectType'],
                    PushedTenderInfo.workContent: info['workContent'],
                    PushedTenderInfo.deposit: info['deposit'],
                    PushedTenderInfo.planScore: info['planScore'],
                    PushedTenderInfo.tenderType: info['tenderType']
                }
                query.update(
                    updateInfo, synchronize_session=False
                )
                db.session.commit()
                return (True, None)
            else:
                return (False, ErrorInfo['TENDER_28'])#推送消息不存在
        except Exception as e:
            print e
            traceback.print_exc()
            errorInfo = ErrorInfo['TENDER_02']
            errorInfo['detail'] = str(e)
            db.session.rollback()
            return (False, errorInfo)

    # 已经完成，添加项目信息
    def updateDonePushedTender(self, info):
        userID = info['userID']
        tenderID = info['tenderID']
        query = db.session.query(Operator).filter(
            Operator.tenderID == tenderID
        )
        result = query.first()
        if result.userID != userID:
            return (False, ErrorInfo['TENDER_27'])  # 不是经办人，无法填写
        try:
            query = db.session.query(PushedTenderInfo).filter(
                PushedTenderInfo.tenderID == tenderID
            )
            result = query.first()
            if result:
                updateInfo = {
                    PushedTenderInfo.averagePrice: info['averagePrice'],
                    PushedTenderInfo.benchmarkPrice: info['benchmarkPrice'],
                    PushedTenderInfo.K1: info['K1'],
                    PushedTenderInfo.K2: info['K2'],
                    PushedTenderInfo.Q1: info['Q1'],
                    PushedTenderInfo.Q2: info['Q2'],
                    PushedTenderInfo.deductedRate1: info['deductedRate1'],
                    PushedTenderInfo.deductedRate2: info['deductedRate2'],
                    PushedTenderInfo.workerName: info['workerName'],
                    PushedTenderInfo.candidateName1: info['candidateName1'],
                    PushedTenderInfo.candidatePrice1: info['candidatePrice1'],
                    PushedTenderInfo.candidateName2: info['candidateName2'],
                    PushedTenderInfo.candidatePrice2: info['candidatePrice2'],
                    PushedTenderInfo.candidateName3: info['candidateName3'],
                    PushedTenderInfo.candidatePrice3: info['candidatePrice3'],
                    PushedTenderInfo.ceilPrice: info['ceilPrice'],
                    PushedTenderInfo.winbidding: info['winbidding']
                }
                query.update(
                    updateInfo, synchronize_session=False
                )
                db.session.commit()
                return (True, None)
            else:
                return (False, ErrorInfo['TENDER_28'])  # 推送消息不存在
        except Exception as e:
            print e
            errorInfo = ErrorInfo['TENDER_02']
            errorInfo['detail'] = str(e)
            db.session.rollback()
            return (False, errorInfo)


    # 添加报价信息,负责人，审核人，或者审定人
    def createQuotedPrice(self, info):
        userID = info['userID']
        tenderID = info['tenderID']
        userType = info['userType']
        createTime = datetime.now()
        quotedID = self.generateID(userID + tenderID)
        info['quotedID'] = quotedID
        info['createTime'] = createTime
        try:
            query = db.session.query(QuotedPrice).filter(
                and_(
                    QuotedPrice.userID == userID,
                    QuotedPrice.tenderID == tenderID
                )
            )
            result = query.first()
            if result is not None:
                return (False, ErrorInfo['TENDER_29'])#已经填写了报价信息
            QuotedPrice.create(info=info)
            if userType == USER_TAG_BOSS:
                pushedQuery = db.session.query(PushedTenderInfo).filter(
                    PushedTenderInfo.tenderID == tenderID
                )
                pushedQuery.update({
                    PushedTenderInfo.quotedDescription : info['description'],
                    PushedTenderInfo.quotedDate : createTime,
                    PushedTenderInfo.quotedPrice : info['price']
                }, synchronize_session=False)
            db.session.commit()
            return (True, None)
        except Exception as e:
            print e
            traceback.print_exc()
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

    #
    def createAssignMessage(self, info):
        tag = info['tag']
        pushedID = info['pushedID']
        messageManager = MessageManager()
        toUserQuery = db.session.query(UserInfo).filter(
            UserInfo.userType == MESSAGE_ASSIGN_DIC[tag]
        )
        toUserResult = toUserQuery.first()
        if toUserResult:
            info['toUserID'] = toUserResult.userID
            info['description'] = MESSAGE_ASSIGN_DIC['description']
            info['messageTag'] = MESSAGE_ASSIGN_DIC['tag']
            info['foreignID'] = pushedID
            (status, result) = messageManager.createOAMessage(info=info)
            return (True, None)
        else:
            return (False, None)

    # 负责人或审核人推送, 从上一级或上两级中继续推送
    def updatePushedTenderInfo(self, info):
        pushedID = info['pushedID']
        userType = info['userType']
        info['tag'] = userType
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
            if userType == USER_TAG_BOSS:
                self.createAssignMessage(info=info)
            else:
                self.createPushMessage(info=info)
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
        # 获取推送人员列表
        if self.resp is not None:
            pushedUserList = []
            # 经办人推送了
            if result.PushedTenderInfo.operatorPersonPushedTime is not None:
                u = {}
                u['userID'] = result.UserInfo.userID
                u['userName'] = result.UserInfo.userName
                u['userType'] = result.UserInfo.userType
                pushedUserList.append(u)
            if result.PushedTenderInfo.responsiblePersonPushedTime \
                    is not None and self.selfUserType <= USER_TAG_RESPONSIBLEPERSON:
                u = {}
                u['userID'] = self.resp['userID']
                u['userName'] = self.resp['userName']
                u['userType'] = self.resp['userType']
                pushedUserList.append(u)
            if result.PushedTenderInfo.auditorPushedTime \
                    is not None and self.selfUserType <= USER_TAG_AUDITOR:
                u = {}
                u['userID'] = self.auditor['userID']
                u['userName'] = self.auditor['userName']
                u['userType'] = self.auditor['userType']
                pushedUserList.append(u)
            res['pushedUserList'] = pushedUserList
        return res

    def __generateCustomizedPushedBrief(self, result):
        res = {}
        res.update(PushedTenderInfo.generateBrief(c=result.PushedTenderInfo))
        res.update(CustomizedTender.generate(c=result.CustomizedTender))
        return res

    def getAllPushedList(self, info):
        userID = info['selfUserID']
        userManager = UserManager()
        info['userID'] = userID
        # 获取自己的信息
        (status, userInfo) = userManager.getUserInfo(info=info)
        info['customizedCompanyID'] = userInfo['customizedCompanyID']
        info['selfUserType'] = userInfo['userType']
        info['tenderTag'] = '-1'

        info['staffUserType'] = '-1'
        # 获取用户的信息
        if info['staffUserID'] != '-1':
            info['userID'] = info['staffUserID']
            (status, userInfo) = userManager.getUserInfo(info=info)
            info['staffUserType'] = userInfo['userType']
        return self.getPushedTenderListByUserID(info=info)

    # 经办人 获取我的推送列表, 其他人获取经办人推送列表
    def getPushedTenderListByUserID(self, info):
        startIndex = info['startIndex']
        pageCount = info['pageCount']
        userID = info['staffUserID']
        tenderTag = info['tenderTag']
        staffUserType = info['staffUserType']

        try:
            query = db.session.query(
                PushedTenderInfo, Tender, UserInfo
            ).outerjoin(
                Tender, PushedTenderInfo.tenderID == Tender.tenderID
            ).outerjoin(
                UserInfo, PushedTenderInfo.userID == UserInfo.userID
            ).filter(
                PushedTenderInfo.state != PUSH_TENDER_INFO_TAG_STATE_DISCARD
            )

            countQuery = db.session.query(func.count(PushedTenderInfo.pushedID)).filter(
                PushedTenderInfo.state != PUSH_TENDER_INFO_TAG_STATE_DISCARD
            )

            if tenderTag != '-1':
                query = query.filter(Tender.tenderTag == tenderTag)
                countQuery = countQuery.filter(Tender.tenderTag == tenderTag)


            if userID != '-1':
                # 获取本人的, 或者获取某个人的
                # 如果非经办人 不能看userID字段
                if staffUserType == USER_TAG_OPERATOR:
                    query = query.filter(PushedTenderInfo.userID == userID)
                    countQuery = countQuery.filter(PushedTenderInfo.userID == userID)
                elif staffUserType == USER_TAG_RESPONSIBLEPERSON:
                    query = query.filter(PushedTenderInfo.responsiblePersonPushedTime != None)
                    countQuery = countQuery.filter(PushedTenderInfo.responsiblePersonPushedTime != None)
                elif staffUserType == USER_TAG_AUDITOR:
                    query = query.filter(PushedTenderInfo.auditorPushedTime != None)
                    countQuery = countQuery.filter(PushedTenderInfo.auditorPushedTime != None)

            # else:
            #     print 'hhhhhh'
            #     #  -1 就是获取该用户角色下能获取的
            #     selfUserType = info['selfUserType']
            #     userResult = db.session.query(UserInfo).filter(
            #         UserInfo.userType <= selfUserType
            #     ).all()
            #     staffUserIDTuple = (o.userID for o in userResult)
            #     query = query.filter(
            #         PushedTenderInfo.userID.in_(staffUserIDTuple)
            #     )

            count = countQuery.first()
            count = count[0]
            allResult = query.order_by(desc(PushedTenderInfo.createTime)).offset(startIndex).limit(pageCount).all()

            if info.has_key('customizedCompanyID'):
                userManager = UserManager()
                info['userType'] = USER_TAG_RESPONSIBLEPERSON
                (status, resp) = userManager.getStaffInfo(info=info)
                if status is True:
                    self.resp = resp

                info['userType'] = USER_TAG_AUDITOR
                (status, auditor) = userManager.getStaffInfo(info=info)
                if status is True:
                    self.auditor = auditor

                self.selfUserType = info['selfUserType']

            dataList = [self.__generatePushedBrief(result=result) for result in allResult]

            pushedIDList = [o['pushedID'] for o in dataList]
            info['pushedIDList'] = pushedIDList
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

    # 获取自定义项目的详情
    def getCustomizedTenderDetail(self, jsonInfo):
        info = json.loads(jsonInfo)
        tenderID = info['tenderID']

        try:
            tenderResult = db.session.query(Tender).filter(
                Tender.tenderID == tenderID
            ).first()
            result = {}
            result['tenderID'] = tenderID
            result['title'] = tenderResult.title
            result['url'] = tenderResult.url
            imgResult = db.session.query(ImgPath).filter(
                ImgPath.foreignID == tenderID
            ).all()
            ossInfo = {}
            ossInfo['bucket'] = 'sjtender'
            imgList = [ImgPath.generate(img=o, directory=CUS_TENDER_DOC_DIRECTORY, ossInfo=ossInfo,
                                                hd=True, isFile=True) for o in imgResult]
            result['imgList'] = imgList
            return (True, result)
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
                and_(Operator.userID == userID,
                     PushedTenderInfo.step == step)
            ).order_by(desc(
                PushedTenderInfo.operatorPersonPushedTime
            ))
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
            ).filter(
                PushedTenderInfo.step == step
            ).order_by(desc(
                PushedTenderInfo.operatorPersonPushedTime
            ))
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
        tenderTag = info['tenderTag']

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
                    and_(PushedTenderInfo.responsiblePersonPushedTime != None,
                         Tender.tenderTag == tenderTag)
                ).order_by(desc(
                    PushedTenderInfo.responsiblePersonPushedTime
                ))
                countQuery = countQuery.filter(
                    and_(PushedTenderInfo.responsiblePersonPushedTime != None,
                         PushedTenderInfo.tag == tenderTag)
                )
            #     审核人查询
            elif userType == USER_TAG_AUDITOR:
                query = query.filter(
                    and_(PushedTenderInfo.auditorPushedTime != None,
                         Tender.tenderTag == tenderTag)
                ).order_by(desc(
                    PushedTenderInfo.auditorPushedTime
                ))
                countQuery = countQuery.filter(
                    and_(PushedTenderInfo.auditorPushedTime != None,
                         PushedTenderInfo.tag == tenderTag)
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
            )).order_by(desc(
                PushedTenderInfo.operatorPersonPushedTime
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

    def __generateBookInfo(self, bookResult):
        mDic = {}
        ossInfo = {}
        ossInfo['bucket'] = 'sjtender'
        def generateInfo(result):
            operation = result.Operation
            imgPath = result.ImgPath
            operationID = operation.operationID
            if not mDic.has_key(operationID):
                res = Operation.generate(c=operation)
                if imgPath is None:
                    return res
                imgList = []
                imgList.append(ImgPath.generate(img=imgPath, directory=BID_DOC_DIRECTORY, ossInfo=ossInfo,
                                                hd=True, isFile=True))
                res['fileList'] = imgList
                mDic[operationID] = imgList
                return res
            else:
                imgList = mDic[operationID]
                imgList.append(ImgPath.generate(img=imgPath, directory=BID_DOC_DIRECTORY, ossInfo=ossInfo))
        bookDataList = [generateInfo(result=result) for result in bookResult]
        bookDataList = filter(None, bookDataList)
        return bookDataList

    def getTenderDoingDetail(self, info):
        operatorID = info['operatorID']

        try:
            OperatorResult = db.session.query(Operator).filter(
                Operator.operatorID == operatorID
            ).first()
            tenderID = OperatorResult.tenderID
            info['tenderID'] = tenderID
            # query = db.session.query(Operation).filter(Operation.operatorID == operatorID)
            # allResult = query.all()
            # dataList = [Operation.generate(c=result) for result in allResult]
            # l1 = []
            # l2 = []
            # l4 = []
            # for o in dataList:
            #     if o['tag'] == OPERATION_TAG_ENLIST:
            #         l1.append(o)
            #     elif o['tag'] == OPERATION_TAG_DEPOSIT:
            #         l2.append(o)
            #     elif o['tag'] == OPERATION_TAG_ATTEND:
            #         l4.append(o)


            # 确定投标价格
            info['operationTag'] = OPERATION_TAG_TENDER_PRICE
            l1 = self.__getOperationList(info=info)

            # 保证金支付
            info['operationTag'] = OPERATION_TAG_DEPOSIT
            l2 = self.__getOperationList(info=info)

            # 投标方案
            info['operationTag'] = OPERATION_TAG_TENDER_PLAN
            l3 = self.__getOperationList(info=info)

            # 标书制作
            info['operationTag'] = OPERATION_TAG_MAKE_BIDDING_BOOK
            l4 = self.__getOperationList(info=info)

            # 项目经理安排
            info['operationTag'] = OPERATION_TAG_MANAGER_ARRANGEMENT
            l5 = self.__getOperationList(info=info)

            resultDic = {}
            resultDic[OPERATION_TAG_TENDER_PRICE] = l1
            resultDic[OPERATION_TAG_DEPOSIT] = l2
            resultDic[OPERATION_TAG_TENDER_PLAN] = l3
            resultDic[OPERATION_TAG_MAKE_BIDDING_BOOK] = l4
            resultDic[OPERATION_TAG_MANAGER_ARRANGEMENT] = l5
            # 获取项目信息模块
            (status, projectInfo) = self.__getProjectInfoInDoingDetail(info=info)
            (status, tenderComment) = self.__getTenderCommentInDoingDetail(info=info)
            resultDic['projectInfo'] = projectInfo
            resultDic['tenderComment'] = tenderComment
            (status, quoteResult) = self.__getQuotedPriceByTenderID(info=info)
            resultDic['quoteResult'] = quoteResult
            return (True, resultDic)
        except Exception as e:
            print e
            traceback.print_exc()
            errorInfo = ErrorInfo['TENDER_02']
            errorInfo['detail'] = str(e)
            db.session.rollback()
            return (False, errorInfo)

    def __getOperationList(self, info):
        operatorID = info['operatorID']
        operationTag = info['operationTag']
        operationQuery = db.session.query(Operation, ImgPath).outerjoin(
            ImgPath, Operation.operationID == ImgPath.foreignID
        ).filter(
            and_(
                Operation.tag == operationTag,
                Operation.operatorID == operatorID
            )
        ).order_by(desc(Operation.createTime))
        operationResult = operationQuery.all()

        operationDataList = self.__generateBookInfo(bookResult=operationResult)
        return operationDataList

    def __getQuotedPriceByTenderID(self, info):
        operatorID = info['operatorID']
        userType = info['userType']
        # 获取该自己公司的负责人 审核人 审定人
        operatorResult = db.session.query(Operator).filter(
            Operator.operatorID == operatorID
        ).first()

        if operatorResult is None:
            return (False, ErrorInfo['TENDER_32'])
        userID = operatorResult.userID

        # 获取公司ID, 以后公司多了后 防止出现同一个标被多个公司的人获取
        userResult1 = db.session.query(UserInfo).filter(
            UserInfo.userID == userID
        ).first()
        if userResult1 is None:
            return (False, ErrorInfo['TENDER_23'])
        companyID = userResult1.customizedCompanyID
        info['companyID'] = companyID

        result = {}
        if userType == USER_TAG_RESPONSIBLEPERSON:
            # 获取负责人
            info['userType'] = USER_TAG_RESPONSIBLEPERSON
            (status, respQuote) = self.__getQuoteItem(info=info)
            result['respQuote'] = respQuote
        elif userType == USER_TAG_AUDITOR:
            info['userType'] = USER_TAG_RESPONSIBLEPERSON
            (status, respQuote) = self.__getQuoteItem(info=info)
            result['respQuote'] = respQuote
            info['userType'] = USER_TAG_AUDITOR
            (status, auditorQuote) = self.__getQuoteItem(info=info)
            result['auditorQuote'] = auditorQuote
        elif userType == USER_TAG_BOSS:
            info['userType'] = USER_TAG_RESPONSIBLEPERSON
            (status, respQuote) = self.__getQuoteItem(info=info)
            result['respQuote'] = respQuote
            info['userType'] = USER_TAG_AUDITOR
            (status, auditorQuote) = self.__getQuoteItem(info=info)
            result['auditorQuote'] = auditorQuote
            info['userType'] = USER_TAG_BOSS
            (status, bossQuote) = self.__getQuoteItem(info=info)
            result['bossQuote'] = bossQuote
        else:
            pass
        return (True, result)



    def __getQuoteItem(self, info):
        companyID = info['companyID']
        tenderID = info['tenderID']
        userType = info['userType']
        respResult = db.session.query(UserInfo).filter(and_(
                UserInfo.customizedCompanyID == companyID,
                UserInfo.userType == userType
            )).first()
        leaderUserID = respResult.userID
        # # 测试期间使用
        if userType == USER_TAG_BOSS:
            leaderUserID = '2017-03-3011152863861f7ccd1b1b62b8d8f6b62f713213'
        elif userType == USER_TAG_RESPONSIBLEPERSON:
            leaderUserID = '2017-03-3011152863861f7ccd1b1b62b8d8f6b62d723213'
        elif userType == USER_TAG_AUDITOR:
            leaderUserID = '2017-03-3011152863861f7ccd1b1b62b8d8f6b62f723213'
        quote = {}
        quote['quotedID'] = ''
        quote['quotedPrice'] = ''
        quote['price'] = ''
        quote['costPrice'] = ''
        quote['createTime'] = ''
        quote['description'] = ''
        respQResult = db.session.query(QuotedPrice).filter(and_(
            QuotedPrice.tenderID == tenderID,
            QuotedPrice.userID == leaderUserID
        )).first()
        if respQResult is not None:
            quote['quotedID'] = respQResult.quotedID
            quote['quotedPrice'] = respQResult.quotedPrice
            quote['price'] = respQResult.price
            quote['costPrice'] = respQResult.costPrice
            quote['createTime'] = str(respQResult.createTime)[0:10]
            quote['description'] = respQResult.description
        return (True, quote)

    def __getProjectInfoInDoingDetail(self, info):
        tenderID = info['tenderID']
        res = {}
        res['projectManagerName'] = ''
        res['openedDate'] = ''
        res['openedLocation'] = ''
        res['ceilPrice'] = ''
        res['tenderInfoDescription'] = ''
        res['quotedPrice'] = ''
        res['quotedDate'] = ''
        res['quotedDescription'] = ''
        res['tenderCompanyName'] = ''
        res['projectType'] = ''
        res['workContent'] = ''
        res['deposit'] = ''
        res['planScore'] = ''
        res['tenderType'] = ''

        result = db.session.query(PushedTenderInfo, Tender).outerjoin(
            Tender, PushedTenderInfo.tenderID == Tender.tenderID
        ).filter(
            PushedTenderInfo.tenderID == tenderID
        ).first()
        if result is not None:
            res['projectManagerName'] = result.PushedTenderInfo.projectManagerName
            if result.PushedTenderInfo.openedDate is not None:
                res['openedDate'] = str(result.PushedTenderInfo.openedDate)
            res['openedLocation'] = result.PushedTenderInfo.openedLocation
            if result.PushedTenderInfo.ceilPrice > 0:
                res['ceilPrice'] = result.PushedTenderInfo.ceilPrice
            res['tenderInfoDescription'] = result.PushedTenderInfo.tenderInfoDescription
            res['pushedID'] = result.PushedTenderInfo.pushedID
            res['tenderCompanyName'] = result.PushedTenderInfo.tenderCompanyName
            res['projectType'] = result.PushedTenderInfo.projectType
            res['workContent'] = result.PushedTenderInfo.workContent
            res['deposit'] = result.PushedTenderInfo.deposit
            res['planScore'] = result.PushedTenderInfo.planScore
            res['tenderType'] = result.PushedTenderInfo.tenderType
            res.update(Tender.generateBrief(tender=result.Tender))
            # 只有经办人能看到
            if info['userType'] == USER_TAG_OPERATOR:
                if result.PushedTenderInfo.quotedPrice > 0:
                    res['quotedPrice'] = result.PushedTenderInfo.quotedPrice
                if result.PushedTenderInfo.quotedDate is not None:
                    res['quotedDate'] = str(result.PushedTenderInfo.quotedDate)
                res['quotedDescription'] = result.PushedTenderInfo.quotedDescription
            elif info['userType'] == USER_TAG_RESPONSIBLEPERSON:
                (status, respQuotedPrice) = self.__getRespQuotedPrice(info=info)
                res['respQuotedPrice'] = respQuotedPrice
            elif info['userType'] == USER_TAG_AUDITOR:
                (status, respQuotedPrice) = self.__getRespQuotedPrice(info=info)
                res['respQuotedPrice'] = respQuotedPrice
                (status, auditorQuotedPrice) = self.__getAuditorQuotedPrice(info=info)
                res['auditorQuotedPrice'] = auditorQuotedPrice
            elif info['userType'] == USER_TAG_BOSS:
                (status, respQuotedPrice) = self.__getRespQuotedPrice(info=info)
                res['respQuotedPrice'] = respQuotedPrice
                (status, auditorQuotedPrice) = self.__getAuditorQuotedPrice(info=info)
                res['auditorQuotedPrice'] = auditorQuotedPrice
                (status, bossQuotedPrice) = self.__getBossQuotedPrice(info=info)
                res['bossQuotedPrice'] = bossQuotedPrice

        return (True, res)

    def __getRespQuotedPrice(self, info):
        userID = info['userID']
        tenderID = info['tenderID']
        userType = info['userType']
        if userType != USER_TAG_RESPONSIBLEPERSON:
            # 先获取负责人的报价 再获取自己的报价
            selfResult = db.session.query(UserInfo).filter(
                UserInfo.userID == userID
            ).first()
            companyID = selfResult.customizedCompanyID
            respResult = db.session.query(UserInfo).filter(and_(
                UserInfo.customizedCompanyID == companyID,
                UserInfo.userType == USER_TAG_RESPONSIBLEPERSON
            )).first()
            respUserID = respResult.userID
            userName = respResult.userName
        else:
            respUserID = userID
            userName = ''

        # 获取负责人的报价
        respQuotedPrice = {}
        respQuotedPrice['quotedPrice'] = ''
        respQuotedPrice['price'] = ''
        respQuotedPrice['costPrice'] = ''
        respQuotedPrice['createTime'] = ''
        respQuotedPrice['description'] = ''

        respQuotedPriceResult = db.session.query(QuotedPrice).filter(and_(
            QuotedPrice.tenderID == tenderID,
            QuotedPrice.userID == respUserID
        )).first()
        if respQuotedPriceResult is not None:
            respQuotedPrice['quotedPrice'] = respQuotedPriceResult.quotedPrice
            respQuotedPrice['price'] = respQuotedPriceResult.price
            respQuotedPrice['costPrice'] = respQuotedPriceResult.costPrice
            respQuotedPrice['createTime'] = str(respQuotedPriceResult.createTime)
            respQuotedPrice['description'] = respQuotedPriceResult.description
            respQuotedPrice['userName'] = userName
        return (True, respQuotedPrice)

    def __getAuditorQuotedPrice(self, info):
        userID = info['userID']
        tenderID = info['tenderID']
        userType = info['userType']
        # 先获取负责人的报价 再获取自己的报价
        if userType != USER_TAG_AUDITOR:
            selfResult = db.session.query(UserInfo).filter(
                UserInfo.userID == userID
            ).first()
            companyID = selfResult.customizedCompanyID
            auditorResult = db.session.query(UserInfo).filter(and_(
                UserInfo.customizedCompanyID == companyID,
                UserInfo.userType == USER_TAG_AUDITOR
            )).first()
            auditorUserID = auditorResult.userID
            userName = auditorResult.userName
        else:
            auditorUserID = userID
            userName = ''

        # 获取负责人的报价
        selfQuotedPrice = {}
        selfQuotedPrice['quotedPrice'] = ''
        selfQuotedPrice['price'] = ''
        selfQuotedPrice['costPrice'] = ''
        selfQuotedPrice['createTime'] = ''
        selfQuotedPrice['description'] = ''


        # 获取自己的报价
        selfQuotedPriceResult = db.session.query(QuotedPrice).filter(and_(
            QuotedPrice.tenderID == tenderID,
            QuotedPrice.userID == auditorUserID
        )).first()
        if selfQuotedPriceResult is not None:
            selfQuotedPrice['quotedPrice'] = selfQuotedPriceResult.quotedPrice
            selfQuotedPrice['price'] = selfQuotedPriceResult.price
            selfQuotedPrice['costPrice'] = selfQuotedPriceResult.costPrice
            selfQuotedPrice['createTime'] = str(selfQuotedPriceResult.createTime)
            selfQuotedPrice['description'] = selfQuotedPriceResult.description
            selfQuotedPrice['userName'] = userName

        return (True, selfQuotedPrice)


    def __getBossQuotedPrice(self, info):
        userID = info['userID']
        tenderID = info['tenderID']

        selfQuotedPriceResult = db.session.query(QuotedPrice).filter(and_(
            QuotedPrice.tenderID == tenderID,
            QuotedPrice.userID == userID
        )).first()
        selfQuotedPrice = {}
        selfQuotedPrice['quotedPrice'] = ''
        selfQuotedPrice['price'] = ''
        selfQuotedPrice['costPrice'] = ''
        selfQuotedPrice['createTime'] = ''
        selfQuotedPrice['description'] = ''
        if selfQuotedPriceResult is not None:
            selfQuotedPrice['quotedPrice'] = selfQuotedPriceResult.quotedPrice
            selfQuotedPrice['price'] = selfQuotedPriceResult.price
            selfQuotedPrice['costPrice'] = selfQuotedPriceResult.costPrice
            selfQuotedPrice['createTime'] = str(selfQuotedPriceResult.createTime)
            selfQuotedPrice['description'] = selfQuotedPriceResult.description
            selfQuotedPrice['userName'] = ''
        return (True, selfQuotedPrice)


    def __getTenderCommentInDoingDetail(self, info):
        operatorID = info['operatorID']
        query = db.session.query(Operator).filter(Operator.operatorID == operatorID)
        result = query.first()
        if result is not None:
            tenderID = result.tenderID
            query = db.session.query(TenderComment, UserInfo).outerjoin(
                UserInfo, TenderComment.userID == UserInfo.userID
            ).filter(
                TenderComment.tenderID == tenderID
            ).order_by(desc(TenderComment.createTime))
            allResult = query.all()

            def generateInfo(result):
                res = {}
                res['userID'] = ''
                res['userName'] = ''
                res['commentID'] = ''
                res['userID'] = ''
                res['createTime'] = ''
                res['description'] = ''
                res.update(TenderComment.generate(result.TenderComment))
                res.update(UserInfo.generateBrief(result.UserInfo))
                return res

            dataList = [generateInfo(result=result) for result in allResult]
            return (True, dataList)
        else:
            return (False, None)


        # 经办人特殊, 获取自己参与的, 已完成的列表

    def getTenderDoneList(self, jsonInfo):
        info = json.loads(jsonInfo)
        userType = info['userType']
        (status, userID) = self.isTokenValidByUserType(info=info)
        if status is not True:
            errorInfo = ErrorInfo['TENDER_01']
            return (False, errorInfo)
        info['step'] = DONE_STEP
        if userType == USER_TAG_OPERATOR:
            return self.__getTenderDoingList(info=info)
        else:
            return self.__getAllTenderDoingList(info=info)

    def getTenderDoneDetail(self, jsonInfo):
        info = json.loads(jsonInfo)
        tenderID = info['tenderID']
        try:
            query = db.session.query(PushedTenderInfo).filter(PushedTenderInfo.tenderID == tenderID)
            tenderQuery = db.session.query(Tender, City).outerjoin(
                City, Tender.cityID == City.cityID
            ).filter(Tender.tenderID == tenderID)
            result = query.first()
            tenderResult = tenderQuery.first()
            if result and tenderResult:
                callBackInfo = {}
                callBackInfo.update(PushedTenderInfo.generate(c=result))
                callBackInfo.update(Tender.generateBrief(tender=tenderResult.Tender))
                callBackInfo.update(City.generate(city=tenderResult.City))
                return (True, callBackInfo)
            else:
                return (False, ErrorInfo['TENDER_28'])
        except Exception as e:
            print e
            errorInfo = ErrorInfo['TENDER_02']
            errorInfo['detail'] = str(e)
            db.session.rollback()
            return (False, errorInfo)


    # 经办人特殊, 获取自己参与的, 历史记录
    def getTenderHistoryList(self, jsonInfo):
        info = json.loads(jsonInfo)
        userType = info['userType']
        (status, userID) = self.isTokenValidByUserType(info=info)
        if status is not True:
            errorInfo = ErrorInfo['TENDER_01']
            return (False, errorInfo)
        info['step'] = HISTORY_STEP
        if userType == USER_TAG_OPERATOR:
            return self.__getTenderDoingList(info=info)
        else:
            return self.__getAllTenderDoingList(info=info)

    def getTenderHistoryDetail(self, jsonInfo):
        pass

    def getDiscardPushedListWithPushedList(self, info):
        userID = info['selfUserID']
        userManager = UserManager()
        info['userID'] = userID
        # 获取自己的信息
        (status, userInfo) = userManager.getUserInfo(info=info)
        info['customizedCompanyID'] = userInfo['customizedCompanyID']
        info['selfUserType'] = userInfo['userType']
        info['tenderTag'] = '-1'

        info['staffUserType'] = '-1'
        # 获取用户的信息
        if info['staffUserID'] != '-1':
            info['userID'] = info['staffUserID']
            (status, userInfo) = userManager.getUserInfo(info=info)
            info['staffUserType'] = userInfo['userType']
        return self.getPushedTenderListByUserID(info=info)

    # def getDiscardPushedList(self, info):
    #     tokenID = info['tokenID']
    #     (status, userID) = self.isTokenValid(tokenID)
    #     if status is not True:
    #         errorInfo = ErrorInfo['TENDER_01']
    #         return (False, errorInfo)
    #
    #     info['selfUserID'] = userID
    #     info['selfUserType'] = USER_TAG_RESPONSIBLEPERSON
    #     info['staffUserID'] = '-1'
    #     return self.getDiscardPushedListWithPushedList(info=info)


        # startIndex = info['startIndex']
        # pageCount = info['pageCount']
        # try:
        #     query = db.session.query(
        #         PushedTenderInfo, Tender
        #     ).outerjoin(
        #         Tender, PushedTenderInfo.tenderID == Tender.tenderID
        #     ).filter(
        #         PushedTenderInfo.state == PUSH_TENDER_INFO_TAG_STATE_DISCARD
        #     )
        #     countQuery = db.session.query(
        #         func.count(PushedTenderInfo.pushedID)
        #     ).filter(
        #         PushedTenderInfo.state == PUSH_TENDER_INFO_TAG_STATE_DISCARD
        #     )
        #
        #     allResult = query.offset(startIndex).limit(pageCount).all()
        #     count = countQuery.first()
        #     dataList = [self.__generatePushedBrief(result=result) for result in allResult]
        #     callBackInfo = {}
        #     callBackInfo['dataList'] = dataList
        #     callBackInfo['count'] = count[0]
        #     return (True, callBackInfo)
        # except Exception as e:
        #     traceback.print_exc()
        #     print e
        #     errorInfo = ErrorInfo['TENDER_02']
        #     errorInfo['detail'] = str(e)
        #     db.session.rollback()
        #     return (False, errorInfo)

    def recoverPushedTenderInfo(self, info):
        tenderID = info['tenderID']


        try:
            query = db.session.query(PushedTenderInfo).filter(
                PushedTenderInfo.tenderID == tenderID
            )
            result = query.first()
            if result is None:
                return (False, ErrorInfo['TENDER_28'])

            state = result.state
            if state != PUSH_TENDER_INFO_TAG_STATE_DISCARD:
                return (False, ErrorInfo['TENDER_36'])

            query.update({
                PushedTenderInfo.state : PUSH_TENDER_INFO_TAG_STATE_UNREAD
            }, synchronize_session=False)
            db.session.commit()
            return (True, None)
        except Exception as e:
            traceback.print_exc()
            print e
            errorInfo = ErrorInfo['TENDER_02']
            errorInfo['detail'] = str(e)
            db.session.rollback()
            return (False, errorInfo)


    def __generateDataInfo(self, o, res):
        res['pushedCount'] = res['pushedCount'] + 1
        if o.state == PUSH_TENDER_INFO_TAG_STATE_APPROVE:
            res['usedCount'] = res['usedCount'] + 1
        if o.winbidding is True:
            res['wonCount'] = res['wonCount'] + 1
        return (True, None)


    # 根据用户ID获取用户的推送，采纳及中标各项数据信息
    def getDataInfoByUserID(self, info):
        userID = info['userID']
        userType = info['userType']
        startDate = info['startDate']
        endDate = info['endDate']

        res = {}
        res['pushedCount'] = 0
        res['usedCount'] = 0
        res['wonCount'] = 0
        res['startDate'] = startDate
        res['endDate'] = endDate

        query = db.session.query(PushedTenderInfo).filter(
            PushedTenderInfo.userID == userID
        )
        if userType == USER_TAG_OPERATOR:
            if startDate != '-1':
                query = query.filter(
                    PushedTenderInfo.operatorPersonPushedTime >= startDate
                )
            if endDate != '-1':
                query = query.filter(
                    PushedTenderInfo.operatorPersonPushedTime <= endDate
                )
        elif userType == USER_TAG_RESPONSIBLEPERSON:
            query = db.session.query(PushedTenderInfo).filter(
                PushedTenderInfo.responsiblePersonPushedTime != None
            )
            if startDate != '-1':
                query = query.filter(
                    PushedTenderInfo.responsiblePersonPushedTime >= startDate
                )
            if endDate != '-1':
                query = query.filter(
                    PushedTenderInfo.responsiblePersonPushedTime <= endDate
                )
        elif userType == USER_TAG_AUDITOR:
            query = db.session.query(PushedTenderInfo).filter(
                PushedTenderInfo.auditorPushedTime != None
            )
            if startDate != '-1':
                query = query.filter(
                    PushedTenderInfo.auditorPushedTime >= startDate
                )
            if endDate != '-1':
                query = query.filter(
                    PushedTenderInfo.auditorPushedTime <= endDate
                )
        allResult = query.all()
        _ = [self.__generateDataInfo(o=o, res=res) for o in allResult]
        return (True, res)




if __name__ == '__main__':
    l = [i for i in xrange(0, 10)]

    l1 = [i for i in xrange(0, 5)]

    l2 = [i for i in l if i not in l1]
    print l1
    print l2