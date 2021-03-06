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
from tool.tagconfig import OPERATOR_TAG_CREATED, PUSH_TENDER_INFO_TAG_CUS, PUSH_TENDER_INFO_TAG_TENDER
from tool.tagconfig import USER_TAG_OPERATOR, USER_TAG_RESPONSIBLEPERSON, USER_TAG_AUDITOR, USER_TAG_BOSS

from models.flask_app import db
from models.UserInfo import UserInfo
from models.Operator import Operator
from models.PushedTenderInfo import PushedTenderInfo
from models.Token import Token

from tender.CustomizedTenderManager import CustomizedTenderManager
from pushedTender.PushedTenderManager import PushedTenderManager
from pushedTender.TenderCommentManager import TenderCommentManager
from user.UserBaseManager import UserBaseManager
from user.UserManager import UserManager

class ResponsiblePersonManager(UserBaseManager):
    def __init__(self):
        pass

    # 负责人推送
    def createPushedTenderByResp(self, jsonInfo):
        info = json.loads(jsonInfo)
        info['userType'] = USER_TAG_RESPONSIBLEPERSON
        (status, userID) = PushedTenderManager.isTokenValidByUserType(info=info)
        if status is not True:
            errorInfo = ErrorInfo['TENDER_01']
            return (False, errorInfo)
        info['tag'] = USER_TAG_AUDITOR
        pushedTenderManager = PushedTenderManager()
        info['pushedTenderInfoTag'] = PUSH_TENDER_INFO_TAG_TENDER
        info['userID'] = userID
        return pushedTenderManager.createPushedTender(info=info)

    # 负责人取消推送
    def deletePushedTenderByResp(self, jsonInfo):
        info = json.loads(jsonInfo)
        info['userType'] = USER_TAG_RESPONSIBLEPERSON
        (status, userID) = PushedTenderManager.isTokenValidByUserType(info=info)
        if status is not True:
            errorInfo = ErrorInfo['TENDER_01']
            return (False, errorInfo)
        info['tag'] = USER_TAG_AUDITOR
        pushedTenderManager = PushedTenderManager()
        info['userID'] = userID
        return pushedTenderManager.deletePushedTender(info=info)

    # 创建推送, 自定义标
    def createCustomizedTenderByResp(self, jsonInfo, imgFileList):
        info = json.loads(jsonInfo)
        info['userType'] = USER_TAG_RESPONSIBLEPERSON
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

    def createQuotedPriceByResp(self, jsonInfo):
        info = json.loads(jsonInfo)
        info['userType'] = USER_TAG_RESPONSIBLEPERSON
        (status, userID) = PushedTenderManager.isTokenValidByUserType(info=info)
        if status is not True:
            errorInfo = ErrorInfo['TENDER_01']
            return (False, errorInfo)
        info['userID'] = userID
        pushedTenderManager = PushedTenderManager()
        return pushedTenderManager.createQuotedPrice(info=info)

    # 负责人从经办人推送列表推送
    def updatePushedTenderByResp(self, jsonInfo):
        info = json.loads(jsonInfo)
        info['userType'] = USER_TAG_RESPONSIBLEPERSON
        (status, userID) = PushedTenderManager.isTokenValidByUserType(info=info)
        if status is not True:
            errorInfo = ErrorInfo['TENDER_01']
            return (False, errorInfo)
        pushedTenderManager = PushedTenderManager()
        info['userType'] = USER_TAG_RESPONSIBLEPERSON
        info['userID'] = userID
        return pushedTenderManager.updatePushedTenderInfo(info=info)

    @staticmethod
    def isResponsiblePerson(info):
        userID = info['userID']
        try:
            result = db.session.query(UserInfo).filter(
                UserInfo.userID == userID
            ).first()
        except Exception as e:
            print str(e)
            # traceback.print_stack()
            db.session.rollback()
            errorInfo = ErrorInfo['TENDER_02']
            errorInfo['detail'] = str(e)
            return (False, errorInfo)

        if result is None:
            return (False, ErrorInfo['TENDER_23'])

        tag = UserInfo.userType
        if tag == USER_TAG_RESPONSIBLEPERSON:
            return (True, None)
        return (False, None)

    # 创建经办人, 分配工作
    def createOperator(self, jsonInfo):
        info = json.loads(jsonInfo)
        info['userType'] = USER_TAG_RESPONSIBLEPERSON
        (status, userID) = PushedTenderManager.isTokenValidByUserType(info=info)
        if status is not True:
            errorInfo = ErrorInfo['TENDER_01']
            return (False, errorInfo)

        toUserID = info['userID'].replace('\'', '\\\'').replace('\"', '\\\"')
        tenderID = info['tenderID'].replace('\'', '\\\'').replace('\"', '\\\"')
        operatorID = self.generateID(tenderID)
        operator = Operator(
            operatorID=operatorID, userID=toUserID,
            tenderID=tenderID, state=OPERATOR_TAG_CREATED
        )
        try:
            db.session.add(operator)
            db.session.commit()
        except Exception as e:
            print str(e)
            # traceback.print_stack()
            db.session.rollback()
            errorInfo = ErrorInfo['TENDER_02']
            errorInfo['detail'] = str(e)
            return (False, errorInfo)
        return (True, None)

    # 经办人被否定, 重新分配经办人
    def updateOperator(self, jsonInfo):
        info = json.loads(jsonInfo)
        info['userType'] = USER_TAG_RESPONSIBLEPERSON
        (status, userID) = PushedTenderManager.isTokenValidByUserType(info=info)
        if status is not True:
            errorInfo = ErrorInfo['TENDER_01']
            return (False, errorInfo)
        # 验证登录
        userID = info['userID']
        tenderID = info['tenderID']
        try:
            query = db.session.query(Operator).filter(
                Operator.tenderID == tenderID
            )
            updateInfo = {
                Operator.userID: userID,
                Operator.state : OPERATOR_TAG_CREATED
            }
            query.update(
                updateInfo, synchronize_session=False
            )
            db.session.commit()
        except Exception as e:
            print str(e)
            # traceback.print_stack()
            db.session.rollback()
            errorInfo = ErrorInfo['TENDER_02']
            errorInfo['detail'] = str(e)
            return (False, errorInfo)
        return (True, None)

    # 负责人 获取某个经办人的推送列表
    def getOperatorPushedListByResp(self, jsonInfo):
        info = json.loads(jsonInfo)
        info['userType'] = USER_TAG_RESPONSIBLEPERSON
        (status, userID) = PushedTenderManager.isTokenValidByUserType(info=info)
        if status is not True:
            errorInfo = ErrorInfo['TENDER_01']
            return (False, errorInfo)
        operatorUserID = info['userID']
        info['staffUserID'] = operatorUserID
        pushedTenderManager = PushedTenderManager()
        # info['tenderTag'] = PUSH_TENDER_INFO_TAG_TENDER
        (status, tenderResult) = pushedTenderManager.getPushedTenderListByUserID(info=info)
        if status is True:
            try:
                dataList = tenderResult['dataList']
                tenderIDTuple = (o['tenderID'] for o in dataList)

                pushedResult = db.session.query(PushedTenderInfo).filter(and_(
                    PushedTenderInfo.responsiblePersonPushedTime != None,
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

    # 负责人获取我的推送列表
    def getPushedListByResp(self, jsonInfo):
        info = json.loads(jsonInfo)
        info['userType'] = USER_TAG_RESPONSIBLEPERSON
        (status, userID) = PushedTenderManager.isTokenValidByUserType(info=info)
        if status is not True:
            errorInfo = ErrorInfo['TENDER_01']
            return (False, errorInfo)
        pushedTenderManager = PushedTenderManager()
        return pushedTenderManager.getPushedTenderListByUserType(info=info)


    # 负责人获取待分配列表
    def getUndistributedTenderListByResp(self, jsonInfo):
        info = json.loads(jsonInfo)
        info['userType'] = USER_TAG_RESPONSIBLEPERSON
        (status, userID) = PushedTenderManager.isTokenValidByUserType(info=info)
        if status is not True:
            errorInfo = ErrorInfo['TENDER_01']
            return (False, errorInfo)
        pushedTenderManager = PushedTenderManager()
        return pushedTenderManager.getUndistributedTenderList(info=info)

    # 负责人获取分配列表
    def getDistributedTenderListByResp(self, jsonInfo):
        info = json.loads(jsonInfo)
        info['userType'] = USER_TAG_RESPONSIBLEPERSON
        (status, userID) = PushedTenderManager.isTokenValidByUserType(info=info)
        if status is not True:
            errorInfo = ErrorInfo['TENDER_01']
            return (False, errorInfo)
        pushedTenderManager = PushedTenderManager()
        return pushedTenderManager.getDistributedTenderList(info=info)

    # 负责人 批注正在进行中的项目
    def createTenderCommentByResp(self, jsonInfo):
        info = json.loads(jsonInfo)
        info['userType'] = USER_TAG_RESPONSIBLEPERSON
        (status, userID) = PushedTenderManager.isTokenValidByUserType(info=info)
        if status is not True:
            errorInfo = ErrorInfo['TENDER_01']
            return (False, errorInfo)
        info['userID'] = userID
        tenderCommentManager = TenderCommentManager()
        return tenderCommentManager.createTenderComment(info=info)

    # 负责人, 删除批注
    def deleteTenderCommentByResp(self, jsonInfo):
        info = json.loads(jsonInfo)
        info['userType'] = USER_TAG_RESPONSIBLEPERSON
        (status, userID) = PushedTenderManager.isTokenValidByUserType(info=info)
        if status is not True:
            errorInfo = ErrorInfo['TENDER_01']
            return (False, errorInfo)
        info['userID'] = userID
        tenderCommentManager = TenderCommentManager()
        return tenderCommentManager.deleteTenderComment(info=info)

     # 负责人获取 正在进行中的招标详情
    def getDoingDetailByResp(self, jsonInfo):
        info = json.loads(jsonInfo)
        info['userType'] = USER_TAG_RESPONSIBLEPERSON
        (status, userID) = PushedTenderManager.isTokenValidByUserType(info=info)
        if status is not True:
            errorInfo = ErrorInfo['TENDER_01']
            return (False, errorInfo)
        pushedTenderManager = PushedTenderManager()
        info['userID'] = userID
        return pushedTenderManager.getTenderDoingDetail(info=info)

    # 负责人获取推送人员列表
    def getTenderUserInfoListByResp(self, jsonInfo):
        info = json.loads(jsonInfo)
        info['userType'] = USER_TAG_RESPONSIBLEPERSON
        (status, userID) = PushedTenderManager.isTokenValidByUserType(info=info)
        if status is not True:
            errorInfo = ErrorInfo['TENDER_01']
            return (False, errorInfo)
        userManager = UserManager()
        info['userID'] = userID
        (status, userInfo) = self.getUserInfo(info=info)
        info['customizedCompanyID'] = userInfo['customizedCompanyID']
        return userManager.getTenderUserInfoList(info=info)

    # 给数据打上tag，是否推送了
    def __tagTenderList(self, info):
        dataList = info['dataList']
        for o in dataList:
            if o['responsiblePersonPushedTime'] != '':
                o['pushed'] = True
            else:
                o['pushed'] = False

        return (True, info)

    # 负责人  获取所有人的推送列表
    def getAllPushedListByResp(self, jsonInfo):
        info = json.loads(jsonInfo)
        tokenID = info['tokenID']
        (status, userID) = self.isTokenValid(tokenID)
        if status is not True:
            errorInfo = ErrorInfo['TENDER_01']
            return (False, errorInfo)

        info['selfUserID'] = userID
        info['selfUserType'] = USER_TAG_RESPONSIBLEPERSON
        info['staffUserID'] = info['userID']
        pushedTenderManager = PushedTenderManager()
        (status, result) = pushedTenderManager.getAllPushedList(info=info)
        if status is True:
            self.__tagTenderList(info=result)
        return (status, result)

    # 负责人获取我的推送数据分析
    def getDataInfoByResp(self, jsonInfo):
        info = json.loads(jsonInfo)
        tokenID = info['tokenID']
        (status, userID) = self.isTokenValid(tokenID)
        if status is not True:
            errorInfo = ErrorInfo['TENDER_01']
            return (False, errorInfo)
        info['userType'] = USER_TAG_RESPONSIBLEPERSON
        info['userID'] = userID
        pushedTenderManager = PushedTenderManager()
        return pushedTenderManager.getDataInfoByUserID(info=info)

    # 获取所有员工的推送信息
    def getAllDataInfoByResp(self, jsonInfo):
        info = json.loads(jsonInfo)
        (status, dataInfo) = self.getTenderUserInfoListByResp(jsonInfo=jsonInfo)
        dataList = dataInfo['dataList']

        pushedTenderManager = PushedTenderManager()
        _ = [self.addPushedDataInfoToUser(o=o, pushedTenderManager=pushedTenderManager, info=info) for o in dataList]
        return (True, dataInfo)

    # 负责人创建标书
    def createOperationBiddingBookByResp(self, jsonInfo, imgFileList):
        info = json.loads(jsonInfo)
        info['userType'] = USER_TAG_RESPONSIBLEPERSON
        jsonInfo = json.dumps(info)
        return self.createOperationBiddingBook(jsonInfo=jsonInfo, imgFileList=imgFileList)