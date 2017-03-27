# coding=utf8
import sys
import json
sys.path.append("..")
import os, random, requests
reload(sys)
sys.setdefaultencoding('utf-8')

from datetime import datetime
from sqlalchemy import and_, text, func, desc
from tool.Util import Util
from tool.config import ErrorInfo
from tool.tagconfig import USER_TAG_OPERATOR, USER_TAG_RESPONSIBLEPERSON, USER_TAG_AUDITOR, USER_TAG_BOSS, \
    PUSH_TENDER_INFO_TAG_STEP_DONE, PUSH_TENDER_INFO_TAG_STEP_HISTORY
from tool.tagconfig import OPERATION_TAG_ENLIST, OPERATION_TAG_DEPOSIT, BID_DOC_DIRECTORY
from tool.tagconfig import OPERATION_TAG_MAKE_BIDDING_BOOK, OPERATION_TAG_ATTEND


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
            #如果状态是制作标书，需要上传标书文件
            if info['tag'] == OPERATION_TAG_MAKE_BIDDING_BOOK:
                info['directory'] = BID_DOC_DIRECTORY
                info['foreignID'] = operationID
                imageManager = ImageManager()
                imageManager.addImagesWithOSS(info=info)
            db.session.commit()
        except Exception as e:
            print e
            errorInfo = ErrorInfo['TENDER_02']
            errorInfo['detail'] = str(e)
            db.session.rollback()
            return (False, errorInfo)
        return (True, operationID)


    # 经办人获取我的推送列表
    def getPushedListByOperator(self, jsonInfo):
        info = json.loads(jsonInfo)
        info['userType'] = USER_TAG_OPERATOR
        (status, userID) = PushedTenderManager.isTokenValidByUserType(info=info)
        if status is not True:
            errorInfo = ErrorInfo['TENDER_01']
            return (False, errorInfo)
        info['userID'] = userID
        pushedTenderManager = PushedTenderManager()
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
            errorInfo = ErrorInfo['TENDER_02']
            errorInfo['detail'] = str(e)
            db.session.rollback()
            return (False, errorInfo)


    # 经办人获取所有的招标信息列表
    def getTenderListWithPushedTagByOperator(self, jsonInfo):
        pass

    def __generateBookInfo(self, bookResult):
        mDic = {}
        ossInfo = {}
        ossInfo['bucket'] = 'tender'
        def generateInfo(result):
            operation = result.Operation
            imgPath = result.ImgPath
            operationID = operation.operationID
            if not mDic.has_key(operationID):
                res = Operation.generate(c=operation)
                imgList = []
                imgList.append(ImgPath.generate(img=imgPath, directory=BID_DOC_DIRECTORY, ossInfo=ossInfo))
                res['fileList'] = imgList
                mDic[operationID] = imgList
                return res
            else:
                imgList = mDic[operationID]
                imgList.append(ImgPath.generate(img=imgPath, directory=BID_DOC_DIRECTORY, ossInfo=ossInfo))
        bookDataList = [generateInfo(result=result) for result in bookResult]
        return bookDataList

    #根据operatorID获取operations信息
    def getOperationListByOperatorID(self, jsonInfo):
        info = json.loads(jsonInfo)
        info['userType'] = USER_TAG_OPERATOR
        operatorID = info['operatorID']
        (status, userID) = PushedTenderManager.isTokenValidByUserType(info=info)
        if status is not True:
            errorInfo = ErrorInfo['TENDER_01']
            return (False, errorInfo)
        try:
            query = db.session.query(Operation).filter(Operation.operatorID == operatorID)
            allResult = query.all()
            bookQuery = db.session.query(Operation, ImgPath).outerjoin(
                ImgPath, Operation.operationID == ImgPath.foreignID
            ).filter(
                and_(
                    Operation.tag == OPERATION_TAG_MAKE_BIDDING_BOOK,
                    Operation.operatorID == operatorID
                )
            )
            bookResult = bookQuery.all()
            dataList = [Operation.generate(c=result) for result in allResult]
            bookDataList = self.__generateBookInfo(bookResult=bookResult)
            l1 = []
            l2 = []
            l4 = []
            for o in dataList:
                if o['tag'] == OPERATION_TAG_ENLIST:
                    l1.append(o)
                elif o['tag'] == OPERATION_TAG_DEPOSIT:
                    l2.append(o)
                elif  o['tag'] == OPERATION_TAG_ATTEND:
                    l4.append(o)
            resultDic = {}
            resultDic[OPERATION_TAG_ENLIST] = l1
            resultDic[OPERATION_TAG_DEPOSIT] = l2
            resultDic[OPERATION_TAG_MAKE_BIDDING_BOOK] = []
            resultDic[OPERATION_TAG_ATTEND] = l4
            return (True, resultDic)
        except Exception as e:
            print e
            errorInfo = ErrorInfo['TENDER_02']
            errorInfo['detail'] = str(e)
            db.session.rollback()
            return (False, errorInfo)

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