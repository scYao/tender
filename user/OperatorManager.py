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
from tool.tagconfig import USER_TAG_OPERATOR, USER_TAG_RESPONSIBLEPERSON, USER_TAG_AUDITOR, USER_TAG_BOSS, \
    PUSH_TENDER_INFO_TAG_STEP_DONE, PUSH_TENDER_INFO_TAG_STEP_HISTORY, PUSH_TENDER_INFO_TAG_CUS, \
    PUSH_TENDER_INFO_TAG_TENDER
from tool.tagconfig import OPERATION_TAG_TENDER_PRICE, OPERATION_TAG_DEPOSIT, BID_DOC_DIRECTORY
from tool.tagconfig import OPERATION_TAG_TENDER_PLAN, OPERATION_TAG_MAKE_BIDDING_BOOK


from models.flask_app import db
from models.Operator import Operator
from models.PushedTenderInfo import PushedTenderInfo
from models.Message import Message
from models.UserInfo import UserInfo
from models.Token import Token
from models.Operation import Operation
from models.ImgPath import ImgPath

from ResponsiblePersonManager import ResponsiblePersonManager
from pushedTender.PushedTenderManager import PushedTenderManager
from image.ImageManager import ImageManager
from tender.CustomizedTenderManager import CustomizedTenderManager


class OperatorManager(Util):
    def __init__(self):
        pass

    # 经办人推送
    def createPushedTenderByOperator(self, jsonInfo):
        info = json.loads(jsonInfo)
        info['userType'] = USER_TAG_OPERATOR
        (status, userID) = PushedTenderManager.isTokenValidByUserType(info=info)
        if status is not True:
            errorInfo = ErrorInfo['TENDER_01']
            return (False, errorInfo)
        pushedTenderManager = PushedTenderManager()
        info['userID'] = userID
        info['pushedTenderInfoTag'] = PUSH_TENDER_INFO_TAG_TENDER
        return pushedTenderManager.createPushedTender(info)

    # 经办人取消自己的推送
    def deletePushedTenderByOperator(self, jsonInfo):
        info = json.loads(jsonInfo)
        info['userType'] = USER_TAG_OPERATOR
        (status, userID) = PushedTenderManager.isTokenValidByUserType(info=info)
        if status is not True:
            errorInfo = ErrorInfo['TENDER_01']
            return (False, errorInfo)
        info['userID'] = userID
        pushedTenderManager = PushedTenderManager()
        return pushedTenderManager.deletePushedTender(info)




    # 创建推送, 自定义标
    def createCustomizedTenderByOperator(self, jsonInfo, imgFileList):
        info = json.loads(jsonInfo)
        info['userType'] = USER_TAG_OPERATOR
        (status, userID) = PushedTenderManager.isTokenValidByUserType(info=info)
        if status is not True:
            errorInfo = ErrorInfo['TENDER_01']
            return (False, errorInfo)
        info['userID'] = userID
        customizedTenderManager = CustomizedTenderManager()
        (status, tenderID) = customizedTenderManager.createCustomizedTender(info=info, imgFileList=imgFileList)
        if status is not True:
            return (False, tenderID)
        info['tenderID'] = tenderID
        pushedTenderManager = PushedTenderManager()
        info['pushedTenderInfoTag'] = PUSH_TENDER_INFO_TAG_CUS
        return pushedTenderManager.createPushedTender(info)

    #添加项目信息
    def updateDoingPushedTender(self, jsonInfo):
        info = json.loads(jsonInfo)
        info['userType'] = USER_TAG_OPERATOR
        (status, userID) = PushedTenderManager.isTokenValidByUserType(info=info)
        if status is not True:
            errorInfo = ErrorInfo['TENDER_01']
            return (False, errorInfo)
        info['userID'] = userID
        pushedTenderManager = PushedTenderManager()
        return pushedTenderManager.updateDoingPushedTender(info)

    # 已经完成，添加项目信息
    def updateDonePushedTender(self, jsonInfo):
        info = json.loads(jsonInfo)
        info['userType'] = USER_TAG_OPERATOR
        (status, userID) = PushedTenderManager.isTokenValidByUserType(info=info)
        if status is not True:
            errorInfo = ErrorInfo['TENDER_01']
            return (False, errorInfo)
        info['userID'] = userID
        pushedTenderManager = PushedTenderManager()
        return pushedTenderManager.updateDonePushedTender(info)

    # 记录动作, 打保证金等
    def createOperation(self, jsonInfo):
        info = json.loads(jsonInfo)
        operatorID = info['operatorID']
        operationID = self.generateID(operatorID)
        info['operationID'] = operationID
        info['createTime'] = datetime.now()
        try:
            Operation.create(info=info)
            # #如果状态是制作标书，需要上传标书文件
            # if info['tag'] == OPERATION_TAG_MAKE_BIDDING_BOOK:
            #     info['directory'] = BID_DOC_DIRECTORY
            #     info['foreignID'] = operationID
            #     imageManager = ImageManager()
            #     imageManager.addImagesWithOSS(info=info)
            db.session.commit()
        except Exception as e:
            print e
            errorInfo = ErrorInfo['TENDER_02']
            errorInfo['detail'] = str(e)
            db.session.rollback()
            return (False, errorInfo)
        return (True, operationID)

    # 上传标书
    def createOperationBiddingBook(self, jsonInfo, imgFileList):
        (status, operationID) = self.createOperation(jsonInfo=jsonInfo)
        if status is not True:
            return (False, operationID)
        ossInfo = {}
        ossInfo['bucket'] = 'sjtender'
        try:
            index = 0
            for i in imgFileList:
                imgID = self.generateID(str(index) + i['imgName'])
                postFix = str(i['imgName']).split('.')
                if len(postFix) > 0:
                    postFix = '.' + postFix[-1]
                else:
                    postFix = ''
                imgPath = imgID + postFix
                imagePath = ImgPath(imgPathID=imgID, path=imgPath,
                                    foreignID=operationID, imgName=i['imgName'])
                db.session.add(imagePath)
                index = index + 1
                self.uploadOSSImage('biddocument/%s' % imgPath, ossInfo, i['file'])
            db.session.commit()
            return (True, operationID)
        except Exception as e:
            print e
            print 'upload file to oss error'
            errorInfo = ErrorInfo['TENDER_31']
            errorInfo['detail'] = str(e)
            return (False, errorInfo)



    # 经办人获取我的推送列表
    def getPushedListByOperator(self, jsonInfo):
        info = json.loads(jsonInfo)
        info['userType'] = USER_TAG_OPERATOR
        (status, userID) = PushedTenderManager.isTokenValidByUserType(info=info)
        if status is not True:
            errorInfo = ErrorInfo['TENDER_01']
            return (False, errorInfo)
        info['staffUserID'] = userID
        pushedTenderManager = PushedTenderManager()
        # info['tenderTag'] = PUSH_TENDER_INFO_TAG_TENDER
        info['tenderTag'] = '-1'
        info['staffUserType'] = USER_TAG_OPERATOR
        return pushedTenderManager.getPushedTenderListByUserID(info=info)

    # 获取经办人的推送列表,其他途经
    def getCustomizedPushedListByOperator(self, jsonInfo):
        info = json.loads(jsonInfo)
        info['userType'] = USER_TAG_OPERATOR
        (status, userID) = PushedTenderManager.isTokenValidByUserType(info=info)
        if status is not True:
            errorInfo = ErrorInfo['TENDER_01']
            return (False, errorInfo)
        info['staffUserID'] = userID
        pushedTenderManager = PushedTenderManager()
        info['tenderTag'] = PUSH_TENDER_INFO_TAG_CUS
        return pushedTenderManager.getPushedTenderListByUserID(info=info)

    def __generateUserInfo(self, o):
        res = {}
        res['userID'] = o.userID
        res['userName'] = o.userName
        return res

    # 获取员工列表
    def getUserList(self, jsonInfo):
        info = json.loads(jsonInfo)
        tokenID = info['tokenID']
        (status, userID) = self.isTokenValid(tokenID)
        if status is not True:
            errorInfo = ErrorInfo['TENDER_01']
            return (False, errorInfo)
        try:
            result = db.session.query(UserInfo).filter(
                UserInfo.userID == userID
            ).first()
            companyID = result.customizedCompanyID
            allResult = db.session.query(UserInfo).filter(
                and_(UserInfo.customizedCompanyID == companyID,
                     UserInfo.userType == USER_TAG_OPERATOR)
            ).all()
            dataList = [self.__generateUserInfo(o=o) for o in allResult]
            count = db.session.query(func.count(UserInfo.userID)).filter(
                UserInfo.customizedCompanyID == companyID
            ).first()
            count = count[0]
            userResult = {}
            userResult['dataList'] = dataList
            userResult['count'] = count
            return (True, userResult)
        except Exception as e:
            print e
            traceback.print_exc()
            errorInfo = ErrorInfo['TENDER_02']
            errorInfo['detail'] = str(e)
            db.session.rollback()
            return (False, errorInfo)


    # 经办人获取所有的招标信息列表
    def getTenderListWithPushedTagByOperator(self, jsonInfo):
        pass

    #根据operatorID获取operations信息
    def getOperationListByOperatorID(self, jsonInfo):
        info = json.loads(jsonInfo)
        info['userType'] = USER_TAG_OPERATOR
        (status, userID) = PushedTenderManager.isTokenValidByUserType(info=info)
        if status is not True:
            errorInfo = ErrorInfo['TENDER_01']
            return (False, errorInfo)
        pushedTenderManager = PushedTenderManager()
        info['userID'] = userID
        return pushedTenderManager.getTenderDoingDetail(info=info)

    def __updatePushedTenderInfoStep(self, info):
        operatorID = info['operatorID']
        step = info['step']
        try:
            operatorResult = db.session.query(Operator).filter(
                Operator.operatorID == operatorID
            ).first()

            if operatorResult is None:
                return (False, ErrorInfo['TENDER_30'])
            tenderID = operatorResult.tenderID
            db.session.query(PushedTenderInfo).filter(
                PushedTenderInfo.tenderID == tenderID
            ).update({
                PushedTenderInfo.step : step
            }, synchronize_session=False)
            db.session.commit()
            return (True, None)
        except Exception as e:
            print e
            errorInfo = ErrorInfo['TENDER_02']
            errorInfo['detail'] = str(e)
            db.session.rollback()
            return (False, errorInfo)

    # 由进行中 变为已完成
    def completePushedTenderInfo(self, jsonInfo):
        info = json.loads(jsonInfo)
        (status, userID) = PushedTenderManager.isTokenValidByUserType(info=info)
        if status is not True:
            errorInfo = ErrorInfo['TENDER_01']
            return (False, errorInfo)

        info['step'] = PUSH_TENDER_INFO_TAG_STEP_DONE
        return self.__updatePushedTenderInfoStep(info=info)

    # 由已完成变为历史记录
    def updateToHistory(self, jsonInfo):
        info = json.loads(jsonInfo)
        (status, userID) = PushedTenderManager.isTokenValidByUserType(info=info)
        if status is not True:
            errorInfo = ErrorInfo['TENDER_01']
            return (False, errorInfo)

        info['step'] = PUSH_TENDER_INFO_TAG_STEP_HISTORY
        return self.__updatePushedTenderInfoStep(info=info)

    # 经办人获取我的推送数据分析
    def getDataInfoByOperator(self, jsonInfo):
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