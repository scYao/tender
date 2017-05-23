# coding=utf8
import sys
import json

sys.path.append("..")
import os, random, requests
reload(sys)
sys.setdefaultencoding('utf-8')

import traceback
from datetime import datetime
from sqlalchemy import and_, text, func, desc

from models.flask_app import db
from models.Operation import Operation
from models.ImgPath import ImgPath
from models.UserInfo import UserInfo
from tool.Util import Util
from tool.config import ErrorInfo
from tool.tagconfig import RIGHT_TAG_CONTRACT

from UserManager import UserManager


class UserBaseManager(Util):

    def __init__(self):
        pass

    def addPushedDataInfoToUser(self, o, pushedTenderManager, info):
        info['userID'] = o['userID']
        info['userType'] = o['userType']
        (status, dataInfo) = pushedTenderManager.getDataInfoByUserID(info=info)
        o.update(dataInfo)
        return None

    def getUserInfoByUserID(self, jsonInfo):
        info = json.loads(jsonInfo)
        tokenID = info['tokenID']
        (status, userID) = self.isTokenValid(tokenID)
        if status is not True:
            errorInfo = ErrorInfo['TENDER_01']
            return (False, errorInfo)

        info['userID'] = userID
        return self.getUserInfo(info=info)

    def getUserInfo(self, info):
        userManager = UserManager()
        return userManager.getUserInfo(info=info)

    # 记录动作, 打保证金等
    def createOperation(self, jsonInfo):
        info = json.loads(jsonInfo)
        operatorID = info['operatorID']
        operationID = self.generateID(operatorID)
        info['operationID'] = operationID
        info['createTime'] = datetime.now()
        if not info.has_key('typeID'):
            info['typeID'] = 0
            info['userName'] = ''
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

    def getUserIDListByType(self, info):
        userType = info['userType']
        customizedCompanyID = info['companyID']

        query = db.session.query(UserInfo).filter(and_(
            UserInfo.customizedCompanyID == customizedCompanyID,
            UserInfo.userType == userType
        ))

        allResult = query.all()
        userIDList = [o.userID for o in allResult]

        return (True, userIDList)


    def updateUserDisableInfo(self, info):
        userID = info['userID']
        disable = info['disable']
        try:
            db.session.query(UserInfo).filter(
                UserInfo.userID == userID
            ).update({
                UserInfo.disable : disable
            }, synchronize_session=False)
            db.session.commit()
            return (True, None)
        except Exception as e:
            print e
            traceback.print_stack()
            errorInfo = ErrorInfo['TENDER_02']
            errorInfo['detail'] = str(e)
            db.session.rollback()
            return (False, errorInfo)


    def checkRight(self, info):
        userID = info['userID']
        operationTag = info['operationTag']

        if operationTag == RIGHT_TAG_CONTRACT:
            return (True, None)
        return (True, None)