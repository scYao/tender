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
from models.ContractFinalAccounts import ContractFinalAccounts
from tool.Util import Util
from tool.config import ErrorInfo
from user.UserBaseManager import UserBaseManager

class ContractFinalAccountsManager(Util):
    def __init__(self):
        pass

    def __doCreateContractFinalAccount(self, info):
        submittalDate = info['submittalDate'].replace('\'', '\\\'').replace('\"', '\\\"')
        if info.has_key('submittalPrice'):
            if info['submittalPrice'] == '':
                submittalPrice = None
            else:
                submittalPrice = info['submittalPrice']
        else:
            submittalPrice = None

        if info.has_key('authorizedDate'):
            if info['authorizedDate'] == '':
                authorizedDate = None
            else:
                authorizedDate = info['authorizedDate']
        else:
            authorizedDate = None

        if info.has_key('authorizedPrice'):
            if info['authorizedPrice'] == '':
                authorizedPrice = None
            else:
                authorizedPrice = info['authorizedPrice']
        else:
            authorizedPrice = None

        if info.has_key('cumulativeInvoicePrice'):
            if info['cumulativeInvoicePrice'] == '':
                cumulativeInvoicePrice = None
            else:
                cumulativeInvoicePrice = info['cumulativeInvoicePrice']
        else:
            cumulativeInvoicePrice = None

        if info.has_key('cumulativePayPrice'):
            if info['cumulativePayPrice'] == '':
                cumulativePayPrice = None
            else:
                cumulativePayPrice = info['cumulativePayPrice']
        else:
            cumulativePayPrice = None

        if info.has_key('unPaidBalance'):
            if info['unPaidBalance'] == '':
                unPaidBalance = None
            else:
                unPaidBalance = info['unPaidBalance']
        else:
            unPaidBalance = None
        contractID = info['contractID'].replace('\'', '\\\'').replace('\"', '\\\"')

        accountID = self.generateID(contractID)
        try:
            contractFinalAccounts = ContractFinalAccounts(accountID=accountID, submittalDate=submittalDate,
                                                          submittalPrice=submittalPrice, authorizedPrice=authorizedPrice,
                                                          authorizedDate=authorizedDate, cumulativeInvoicePrice=cumulativeInvoicePrice,
                                                          cumulativePayPrice=cumulativePayPrice, unPaidBalance=unPaidBalance,
                                                          contractID=contractID)
            db.session.add(contractFinalAccounts)
            db.session.commit()
            return (True, accountID)
        except Exception as e:
            print e
            traceback.print_exc()
            errorInfo = ErrorInfo['TENDER_02']
            errorInfo['detail'] = str(e)
            db.session.rollback()
            return (False, errorInfo)

    # 创建决算
    def createContractFinalAccount(self, jsonInfo):
        userBaseManager = UserBaseManager()
        (status, info) = userBaseManager.tokenCheck(jsonInfo=jsonInfo)
        if status is not True:
            return (False, info)
        return self.__doCreateContractFinalAccount(info=info)

    def __doDeleteContractFinalAccount(self, info):
        accountID = info['accountID']
        try:
            db.session.query(ContractFinalAccounts).filter(
                ContractFinalAccounts.accountID == accountID
            ).delete(synchronize_session=False)
            db.session.commit()
            return (True, accountID)
        except Exception as e:
            print e
            traceback.print_exc()
            errorInfo = ErrorInfo['TENDER_02']
            errorInfo['detail'] = str(e)
            db.session.rollback()
            return (False, errorInfo)

    def deleteContractFinalAccount(self, jsonInfo):
        userBaseManager = UserBaseManager()
        (status, info) = userBaseManager.tokenCheck(jsonInfo=jsonInfo)
        if status is not True:
            return (False, info)
        return self.__doDeleteContractFinalAccount(info=info)

    def __doGetContractFinalAccountList(self, info):
        contractID = info['contractID']
        startIndex = info['startIndex']
        pageCount = info['pageCount']

        try:
            query = db.session.query(ContractFinalAccounts).filter(
                ContractFinalAccounts.contractID == contractID
            )
            countQuery = db.session.query(func.count(ContractFinalAccounts.accountID)
                                          ).filter(
                ContractFinalAccounts.contractID == contractID
            )


            allResult = query.offset(startIndex).limit(pageCount).all()
            count = countQuery.first()
            if count is None:
                count = 0
            else:
                count = count[0]

            def __generate(o):
                res = {}
                res.update(ContractFinalAccounts.generate(o=o))
                return res

            dataList = [__generate(o=o) for o in allResult]
            dataInfo = {}
            dataInfo['dataList'] = dataList
            dataInfo['count'] =count
            return (True, dataInfo)
        except Exception as e:
            print e
            traceback.print_exc()
            errorInfo = ErrorInfo['TENDER_02']
            errorInfo['detail'] = str(e)
            db.session.rollback()
            return (False, errorInfo)


    def getContractFinalAccountList(self, jsonInfo):
        userBaseManager = UserBaseManager()
        (status, info) = userBaseManager.tokenCheck(jsonInfo=jsonInfo)
        if status is not True:
            return (False, info)
        return self.__doGetContractFinalAccountList(info=info)

    def checkAccount(self, info):
        contractID = info['contractID']
        try:
            result = db.session.query(ContractFinalAccounts).filter(
                ContractFinalAccounts.contractID == contractID
            ).first()
            if result is not None:
                return (False, ErrorInfo['TENDER_53'])
            return (True, None)
        except Exception as e:
            print e
            traceback.print_exc()
            errorInfo = ErrorInfo['TENDER_02']
            errorInfo['detail'] = str(e)
            db.session.rollback()
            return (False, errorInfo)
