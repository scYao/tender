# coding=utf8
import base64
import sys
import json
import urllib
import urllib2

from Crypto.Cipher import AES
from tool.tagconfig import RIGHT_TAG_CONTRACT

sys.path.append("..")
import os, random, requests
reload(sys)
sys.setdefaultencoding('utf-8')

from datetime import datetime
import hashlib
from sqlalchemy import and_, text, func, desc
import traceback
from models.flask_app import db
from models.Contract import Contract
from tool.Util import Util
from tool.config import ErrorInfo
from user.UserBaseManager import UserBaseManager
from image.ImageManager import ImageManager


class ContractManager(Util):
    def __init__(self):
        pass

    def __doCreateContract(self, info):
        title = info['title'].replace('\'', '\\\'').replace('\"', '\\\"')
        serialNumber = info['serialNumber'].replace('\'', '\\\'').replace('\"', '\\\"')
        createTime = info['createTime']
        projectTypeName = info['projectTypeName']
        operationTypeName = info['operationTypeName']
        contractPrice = info['contractPrice']
        contractWorkContent = info['contractWorkContent'].replace('\'', '\\\'').replace('\"', '\\\"')
        contractor = info['contractor'].replace('\'', '\\\'').replace('\"', '\\\"')
        responsiblePerson = info['responsiblePerson'].replace('\'', '\\\'').replace('\"', '\\\"')
        biddingDate = info['biddingDate']
        contractRecordDate = info['contractRecordDate']
        contractKeepingDeprt = info['contractKeepingDeprt'].replace('\'', '\\\'').replace('\"', '\\\"')
        archiveInfo = info['archiveInfo'].replace('\'', '\\\'').replace('\"', '\\\"')
        contractDuration = info['contractDuration'].replace('\'', '\\\'').replace('\"', '\\\"')


        contractID = self.generateID(title)

        try:
            contract = Contract(contractID=contractID, title=title,
                                serialNumber=serialNumber, createTime=createTime,
                                projectTypeName=projectTypeName, operationTypeName=operationTypeName,
                                contractPrice=contractPrice, contractWorkContent=contractWorkContent,
                                contractor=contractor, responsiblePerson=responsiblePerson, biddingDate=biddingDate,
                                contractRecordDate=contractRecordDate,
                                contractKeepingDeprt=contractKeepingDeprt,
                                archiveInfo=archiveInfo, contractDuration=contractDuration)
            db.session.add(contract)
            db.session.commit()
            return (True, contractID)
        except Exception as e:
            print e
            traceback.print_exc()
            errorInfo = ErrorInfo['TENDER_02']
            errorInfo['detail'] = str(e)
            db.session.rollback()
            return (False, errorInfo)


    def createContract(self, jsonInfo):
        info = json.loads(jsonInfo)
        tokenID = info['tokenID']
        (status, userID) = self.isTokenValid(tokenID)
        if status is not True:
            errorInfo = ErrorInfo['TENDER_01']
            return (False, errorInfo)

        info['userID'] = userID
        userBaseManager = UserBaseManager()
        (status, userInfo) = userBaseManager.getUserInfo(info=info)
        if status is not True:
            return (False, userInfo)

        userBaseManager = UserBaseManager()
        info['operationTag'] = RIGHT_TAG_CONTRACT
        (status, reason) = userBaseManager.checkRight(info=info)
        if status is not True:
            return (False, ErrorInfo['TENDER_50'])

        (status, contractID) = self.__doCreateContract(info=info)
        imgManager = ImageManager()
        info['foreignID'] = contractID
        (status, reason) = imgManager.addImageListWithoutOSS(info=info)
        if status is not True:
            return (False, reason)
        return (True, contractID)

    def __generateContractBrief(self, o):
        res = {}
        res.update(Contract.generate(o=o))
        return res

    # 获取合同列表
    def getContractList(self, jsonInfo):
        userBaseManager = UserBaseManager()
        (status, info) = userBaseManager.tokenCheck(jsonInfo=jsonInfo)
        if status is not True:
            return (False, info)

        startIndex = info['startIndex']
        pageCount = info['pageCount']
        try:
            allResult = db.session.query(
                Contract
            ).offset(startIndex).limit(pageCount).all()
            count = db.session.query(func.count(Contract.contractID)).first()
            if count is None:
                count = 0
            else:
                count = count[0]

            dataList = [self.__generateContractBrief(o=o) for o in allResult]
            dataInfo = {}
            dataInfo['dataList'] = dataList
            dataInfo['count'] = count
            return (True, dataInfo)
        except Exception as e:
            print e
            traceback.print_exc()
            errorInfo = ErrorInfo['TENDER_02']
            errorInfo['detail'] = str(e)
            db.session.rollback()
            return (False, errorInfo)

    # 获取合同详情
    def getContractDetail(self, jsonInfo):
        userBaseManager = UserBaseManager()
        (status, info) = userBaseManager.tokenCheck(jsonInfo=jsonInfo)
        if status is not True:
            return (False, info)

        contractID = info['contractID']
        try:
            result = db.session.query(Contract).filter(
                Contract.contractID == contractID
            ).first()

            dataInfo = {}
            dataInfo.update(Contract.generate(o=result))
            return (True, dataInfo)
        except Exception as e:
            print e
            traceback.print_exc()
            errorInfo = ErrorInfo['TENDER_02']
            errorInfo['detail'] = str(e)
            db.session.rollback()
            return (False, errorInfo)

    # 删除合同
    def deleteContract(self, jsonInfo):
        userBaseManager = UserBaseManager()
        (status, info) = userBaseManager.tokenCheck(jsonInfo=jsonInfo)
        if status is not True:
            return (False, info)

        contractID = info['contractID']
        try:
            # 在删除contract之前，要先删除文件，和其他列表
            db.session.query(Contract).filter(
                Contract.contractID == contractID
            ).delete(synchronize_session=False)
            db.session.commit()
            return (True, None)
        except Exception as e:
            print e
            traceback.print_exc()
            errorInfo = ErrorInfo['TENDER_02']
            errorInfo['detail'] = str(e)
            db.session.rollback()
            return (False, errorInfo)

    # 编辑合同内容
    def updateContract(self, jsonInfo):
        userBaseManager = UserBaseManager()
        (status, info) = userBaseManager.tokenCheck(jsonInfo=jsonInfo)
        if status is not True:
            return (False, info)

        contractID = info['contractID']
        try:
            # 在删除contract之前，要先删除文件，和其他列表
            query = db.session.query(Contract).filter(
                Contract.contractID == contractID
            )
            query.update({
                Contract.title : info['title'],
                Contract.serialNumber : info['serialNumber'],
                Contract.createTime : info['createTime'],
                Contract.projectTypeName : info['projectTypeName'],
                Contract.operationTypeName : info['operationTypeName'],
                Contract.contractPrice : info['contractPrice'],
                Contract.contractWorkContent : info['contractWorkContent'],
                Contract.contractor : info['contractor'],
                Contract.responsiblePerson : info['responsiblePerson'],
                Contract.biddingDate : info['biddingDate'],
                Contract.contractRecordDate : info['contractRecordDate'],
                Contract.contractKeepingDeprt : info['contractKeepingDeprt'],
                Contract.archiveInfo : info['archiveInfo'],
                Contract.contractDuration : info['contractDuration']
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


    def addFileToContract(self, jsonInfo):
        userBaseManager = UserBaseManager()
        (status, info) = userBaseManager.tokenCheck(jsonInfo=jsonInfo)
        if status is not True:
            return (False, info)

        info['foreignID'] = info['contractID']
        imgManager = ImageManager()
        return imgManager.addImageListWithoutOSS(info=info)


    def deleteContractFile(self, jsonInfo):
        userBaseManager = UserBaseManager()
        (status, info) = userBaseManager.tokenCheck(jsonInfo=jsonInfo)
        if status is not True:
            return (False, info)

        imgManager = ImageManager()
        info['directory'] = 'contract'
        return imgManager.deleteImage(info=info)



    def getContractFileList(self, jsonInfo):
        userBaseManager = UserBaseManager()
        (status, info) = userBaseManager.tokenCheck(jsonInfo=jsonInfo)
        if status is not True:
            return (False, info)

        imgManager = ImageManager()
        info['foreignID'] = info['contractID']
        return imgManager.getImageList(info=info)
