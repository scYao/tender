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
from models.UserInfo import UserInfo
from models.Contract import Contract
from tool.Util import Util
from tool.config import ErrorInfo
from tool.StringConfig import STRING_INFO_SMS_REGISTER
from user.UserBaseManager import UserBaseManager
from image.ImageManager import ImageManager


class ContractManager(Util):
    def __init__(self):
        pass

    def __doCreateContract(self, info):
        title = info['title'].replace('\'', '\\\'').replace('\"', '\\\"')
        serialNumber = info['serialNumber'].replace('\'', '\\\'').replace('\"', '\\\"')
        createTime = info['createTime']
        projectTypeID = info['projectTypeID']
        operationTypeID = info['operationTypeID']
        contractPrice = info['contractPrice']
        contractWorkContent = info['contractWorkContent'].replace('\'', '\\\'').replace('\"', '\\\"')
        contractor = info['contractor'].replace('\'', '\\\'').replace('\"', '\\\"')
        biddingDate = info['biddingDate']
        contractRecordDate = info['contractRecordDate']
        contractKeepingDeprt = info['contractKeepingDeprt'].replace('\'', '\\\'').replace('\"', '\\\"')
        archiveInfo = info['archiveInfo'].replace('\'', '\\\'').replace('\"', '\\\"')
        contractDuration = info['contractDuration'].replace('\'', '\\\'').replace('\"', '\\\"')
        resultSubmissionDate = info['resultSubmissionDate'].replace('\'', '\\\'').replace('\"', '\\\"')
        resultReviewDate = info['resultReviewDate'].replace('\'', '\\\'').replace('\"', '\\\"')
        submittalDate = info['submittalDate'].replace('\'', '\\\'').replace('\"', '\\\"')
        submittalPrice = info['submittalPrice']
        authorizedPrice = info['authorizedPrice']
        cumulativeInvoicePrice = info['cumulativeInvoicePrice']
        cumulativePayPrice = info['cumulativePayPrice']
        balance = info['balance']


        contractID = self.generateID(title)

        try:
            contract = Contract(contractID=contractID, title=title,
                                serialNumber=serialNumber, createTime=createTime,
                                projectTypeID=projectTypeID, operationTypeID=operationTypeID,
                                contractPrice=contractPrice, contractWorkContent=contractWorkContent,
                                contractor=contractor, biddingDate=biddingDate,
                                contractRecordDate=contractRecordDate,
                                contractKeepingDeprt=contractKeepingDeprt,
                                archiveInfo=archiveInfo, contractDuration=contractDuration,
                                resultSubmissionDate=resultSubmissionDate,
                                resultReviewDate=resultReviewDate, submittalDate=submittalDate,
                                submittalPrice=submittalPrice, authorizedPrice=authorizedPrice,
                                cumulativeInvoicePrice=cumulativeInvoicePrice,
                                cumulativePayPrice=cumulativePayPrice, balance=balance)
            db.session.add(contract)
            db.session.commit()
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

        imgManager = ImageManager()
        (status, reason) = imgManager.addImageListWithoutOSS(info=info)
        if status is not True:
            return (False, reason)
        return self.__doCreateContract(info=info)