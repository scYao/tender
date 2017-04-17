# coding=utf8
import sys
import json
import traceback

sys.path.append("..")
import os, random, requests
reload(sys)
sys.setdefaultencoding('utf-8')

from datetime import datetime
from sqlalchemy import and_, text, func, desc

from tool.Util import Util
from tool.config import ErrorInfo
from tool.tagconfig import USER_TAG_RESPONSIBLEPERSON, USER_TAG_AUDITOR, USER_TAG_BOSS, PUSH_TENDER_INFO_TAG_TENDER, \
    PUSH_TENDER_INFO_TAG_CUS

from models.flask_app import db
from models.PushedTenderInfo import PushedTenderInfo

from pushedTender.PushedTenderManager import PushedTenderManager
from pushedTender.TenderCommentManager import TenderCommentManager
from tender.CustomizedTenderManager import CustomizedTenderManager
from user.UserBaseManager import UserBaseManager
from user.UserManager import UserManager

class AuditorManager(UserBaseManager):

    def __init__(self):
        pass

    # 审核人推送, 创建推送
    def createPushedTenderByAuditor(self, jsonInfo):
        info = json.loads(jsonInfo)
        info['userType'] = USER_TAG_AUDITOR
        (status, userID) = PushedTenderManager.isTokenValidByUserType(info=info)
        if status is not True:
            errorInfo = ErrorInfo['TENDER_01']
            return (False, errorInfo)
        pushedTenderManager = PushedTenderManager()
        info['pushedTenderInfoTag'] = PUSH_TENDER_INFO_TAG_TENDER
        info['userID'] = userID
        return pushedTenderManager.createPushedTender(info=info)

    # 审核人取消推送
    def deletePushedTenderByAuditor(self, jsonInfo):
        info = json.loads(jsonInfo)
        info['userType'] = USER_TAG_AUDITOR
        (status, userID) = PushedTenderManager.isTokenValidByUserType(info=info)
        if status is not True:
            errorInfo = ErrorInfo['TENDER_01']
            return (False, errorInfo)
        pushedTenderManager = PushedTenderManager()
        return pushedTenderManager.deletePushedTender(info=info)

    # 创建推送, 自定义标
    def createCustomizedTenderByAuditor(self, jsonInfo, imgFileList):
        info = json.loads(jsonInfo)
        info['userType'] = USER_TAG_AUDITOR
        (status, userID) = PushedTenderManager.isTokenValidByUserType(info=info)
        if status is not True:
            errorInfo = ErrorInfo['TENDER_01']
            return (False, errorInfo)
        info['userID'] = userID
        customizedTenderManager = CustomizedTenderManager()
        (status, tenderID) = customizedTenderManager.createCustomizedTender(info=info, imgFileList=imgFileList)
        info['tenderID'] = tenderID
        pushedTenderManager = PushedTenderManager()
        info['pushedTenderInfoTag'] = PUSH_TENDER_INFO_TAG_CUS
        return pushedTenderManager.createPushedTender(info)

    # 审核人填写进行中项目的报价信息
    def createQuotedPriceByAuditor(self, jsonInfo):
        info = json.loads(jsonInfo)
        info['userType'] = USER_TAG_AUDITOR
        (status, userID) = PushedTenderManager.isTokenValidByUserType(info=info)
        if status is not True:
            errorInfo = ErrorInfo['TENDER_01']
            return (False, errorInfo)
        info['userID'] = userID
        pushedTenderManager = PushedTenderManager()
        return pushedTenderManager.createQuotedPrice(info=info)

    # 推送经办人来的推送
    def pushedTenderByAuditor(self, jsonInfo):
        info = json.loads(jsonInfo)
        info['userType'] = USER_TAG_AUDITOR
        (status, userID) = PushedTenderManager.isTokenValidByUserType(info=info)
        if status is not True:
            errorInfo = ErrorInfo['TENDER_01']
            return (False, errorInfo)


    # 审核人获取我的推送列表
    def getPushedListByAuditor(self, jsonInfo):
        info = json.loads(jsonInfo)
        info['userType'] = USER_TAG_AUDITOR
        (status, userID) = PushedTenderManager.isTokenValidByUserType(info=info)
        if status is not True:
            errorInfo = ErrorInfo['TENDER_01']
            return (False, errorInfo)
        info['userType'] = USER_TAG_AUDITOR
        pushedTenderManager = PushedTenderManager()
        return pushedTenderManager.getPushedTenderListByUserType(info=info)



    # 审核人 获取某个经办人的推送列表
    def getOperatorPushedListByAuditor(self, jsonInfo):
        info = json.loads(jsonInfo)
        info['userType'] = USER_TAG_AUDITOR
        operatorUserID = info['userID']
        (status, userID) = PushedTenderManager.isTokenValidByUserType(info=info)
        if status is not True:
            errorInfo = ErrorInfo['TENDER_01']
            return (False, errorInfo)
        info['staffUserID'] = operatorUserID
        pushedTenderManager = PushedTenderManager()
        (status, tenderResult) = pushedTenderManager.getPushedTenderListByUserID(info=info)
        if status is True:
            try:
                dataList = tenderResult['dataList']
                tenderIDTuple = (o['tenderID'] for o in dataList)

                pushedResult = db.session.query(PushedTenderInfo).filter(and_(
                    PushedTenderInfo.auditorPushedTime != None,
                    PushedTenderInfo.tenderID.in_(tenderIDTuple)
                )).all()
                pushedTenderIDList = [o.tenderID for o in pushedResult]
                for o in dataList:
                    if o['tenderID'] in pushedTenderIDList:
                        o['pushed'] = True
                    else:
                        o['pushed'] = False
                return (True, tenderResult)
            except Exception as e:
                print str(e)
                # traceback.print_stack()
                db.session.rollback()
                errorInfo = ErrorInfo['TENDER_02']
                errorInfo['detail'] = str(e)
                return (False, errorInfo)

    # 审核人人从经办人推送列表, 或负责人推送列表推送
    def updatePushedTenderByAuditor(self, jsonInfo):
        info = json.loads(jsonInfo)
        info['userType'] = USER_TAG_AUDITOR
        (status, userID) = PushedTenderManager.isTokenValidByUserType(info=info)
        if status is not True:
            errorInfo = ErrorInfo['TENDER_01']
            return (False, errorInfo)
        pushedTenderManager = PushedTenderManager()
        info['userID'] = userID
        return pushedTenderManager.updatePushedTenderInfo(info=info)

    # 审核人获取所有的招标信息列表
    def getTenderListWithPushedTagByAuditor(self, jsonInfo):
        pass

    # 审核人 获取负责人推送列表
    def getRespPushedListByAuditor(self, jsonInfo):
        info = json.loads(jsonInfo)
        info['userType'] = USER_TAG_AUDITOR
        (status, userID) = PushedTenderManager.isTokenValidByUserType(info=info)
        if status is not True:
            errorInfo = ErrorInfo['TENDER_01']
            return (False, errorInfo)
        info['userType'] = USER_TAG_RESPONSIBLEPERSON
        pushedTenderManager = PushedTenderManager()
        (status, tenderResult) = pushedTenderManager.getPushedTenderListByUserType(info=info)
        if status is True:
            try:
                dataList = tenderResult['dataList']
                tenderIDTuple = (o['tenderID'] for o in dataList)

                pushedResult = db.session.query(PushedTenderInfo).filter(and_(
                    PushedTenderInfo.auditorPushedTime != None,
                    PushedTenderInfo.tenderID.in_(tenderIDTuple)
                )).all()
                pushedTenderIDList = [o.tenderID for o in pushedResult]
                for o in dataList:
                    if o['tenderID'] in pushedTenderIDList:
                        o['pushed'] = True
                    else:
                        o['pushed'] = False
                return (True, tenderResult)
            except Exception as e:
                print str(e)
                traceback.print_stack()
                db.session.rollback()
                errorInfo = ErrorInfo['TENDER_02']
                errorInfo['detail'] = str(e)
                return (False, errorInfo)
        return (False, tenderResult)

    # 负责人 批注正在进行中的项目
    def createTenderCommentByAuditor(self, jsonInfo):
        info = json.loads(jsonInfo)
        info['userType'] = USER_TAG_AUDITOR
        (status, userID) = PushedTenderManager.isTokenValidByUserType(info=info)
        if status is not True:
            errorInfo = ErrorInfo['TENDER_01']
            return (False, errorInfo)
        info['userID'] = userID
        tenderCommentManager = TenderCommentManager()
        return tenderCommentManager.createTenderComment(info=info)


    #审核人删除批注
    def deleteTenderCommentByAuditor(self, jsonInfo):
        info = json.loads(jsonInfo)
        info['userType'] = USER_TAG_AUDITOR
        (status, userID) = PushedTenderManager.isTokenValidByUserType(info=info)
        if status is not True:
            errorInfo = ErrorInfo['TENDER_01']
            return (False, errorInfo)
        info['userID'] = userID
        tenderCommentManager = TenderCommentManager()
        return tenderCommentManager.deleteTenderComment(info=info)

    # 审核人获取 正在进行中的招标详情
    def getDoingDetailByAuditor(self, jsonInfo):
        info = json.loads(jsonInfo)
        info['userType'] = USER_TAG_AUDITOR
        (status, userID) = PushedTenderManager.isTokenValidByUserType(info=info)
        if status is not True:
            errorInfo = ErrorInfo['TENDER_01']
            return (False, errorInfo)
        pushedTenderManager = PushedTenderManager()
        info['userID'] = userID
        return pushedTenderManager.getTenderDoingDetail(info=info)

    # 审核人获取推送人员列表
    def getTenderUserInfoListByAuditor(self, jsonInfo):
        info = json.loads(jsonInfo)
        info['userType'] = USER_TAG_AUDITOR
        (status, userID) = PushedTenderManager.isTokenValidByUserType(info=info)
        if status is not True:
            errorInfo = ErrorInfo['TENDER_01']
            return (False, errorInfo)
        userManager = UserManager()
        info['userID'] = userID
        (status, userInfo) = userManager.getUserInfo(info=info)
        info['customizedCompanyID'] = userInfo['customizedCompanyID']
        return userManager.getTenderUserInfoList(info=info)


    # 给数据打上tag，是否推送了
    def __tagTenderList(self, info):
        dataList = info['dataList']
        for o in dataList:
            if o['auditorPushedTime'] != '':
                o['pushed'] = True
            else:
                o['pushed'] = False
        return (True, info)

    # 审核人  获取所有人的推送列表
    def getAllPushedListByAuditor(self, jsonInfo):
        info = json.loads(jsonInfo)
        tokenID = info['tokenID']
        (status, userID) = self.isTokenValid(tokenID)
        if status is not True:
            errorInfo = ErrorInfo['TENDER_01']
            return (False, errorInfo)

        info['selfUserID'] = userID
        info['staffUserID'] = info['userID']
        pushedTenderManager = PushedTenderManager()
        (status, result) = pushedTenderManager.getAllPushedList(info=info)
        if status is True:
            self.__tagTenderList(info=result)
        return (status, result)

    # 审核人获取我的推送数据分析
    def getDataInfoByAuditor(self, jsonInfo):
        info = json.loads(jsonInfo)
        tokenID = info['tokenID']
        (status, userID) = self.isTokenValid(tokenID)
        if status is not True:
            errorInfo = ErrorInfo['TENDER_01']
            return (False, errorInfo)
        info['userType'] = USER_TAG_AUDITOR
        info['userID'] = userID
        pushedTenderManager = PushedTenderManager()
        return pushedTenderManager.getDataInfoByUserID(info=info)

    # 获取所有员工的推送信息
    def getAllDataInfoByAuditor(self, jsonInfo):
        info = json.loads(jsonInfo)
        (status, dataInfo) = self.getTenderUserInfoListByAuditor(jsonInfo=jsonInfo)
        dataList = dataInfo['dataList']

        pushedTenderManager = PushedTenderManager()
        _ = [self.addPushedDataInfoToUser(o=o, pushedTenderManager=pushedTenderManager, info=info) for o in dataList]
        return (True, dataInfo)