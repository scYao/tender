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
from models.ContractProjectProcess import ContractProjectProcess
from tool.Util import Util
from tool.config import ErrorInfo
from user.UserBaseManager import UserBaseManager

class ContractProjectProcessManager(Util):
    def __init__(self):
        pass

    def __doCreateContractProjectProcess(self, info):
        createTime = info['createTime']
        processRate = info['processRate']
        description = info['description'].replace('\'', '\\\'').replace('\"', '\\\"').strip()
        userName = info['userName'].replace('\'', '\\\'').replace('\"', '\\\"').strip()
        contractID = info['contractID']
        resultSubmissionDate = info['resultSubmissionDate']
        resultReviewDate = info['resultReviewDate']

        processID = self.generateID(contractID)

        try:
            proc = ContractProjectProcess(processID=processID, createTime=createTime,
                                          processRate=processRate, description=description,
                                          userName=userName, contractID=contractID,
                                          resultSubmissionDate=resultSubmissionDate,
                                          resultReviewDate=resultReviewDate)
            db.session.add(proc)
            db.session.commit()
            return (True, processID)
        except Exception as e:
            print e
            traceback.print_exc()
            errorInfo = ErrorInfo['TENDER_02']
            errorInfo['detail'] = str(e)
            db.session.rollback()
            return (False, errorInfo)

    def createContractProjectProcess(self, jsonInfo):
        userBaseManager = UserBaseManager()
        (status, info) = userBaseManager.tokenCheck(jsonInfo=jsonInfo)
        if status is not True:
            return (False, info)

        return self.__doCreateContractProjectProcess(info=info)

    def __doDeleteContractProjectProcess(self, info):
        processID = info['processID']
        try:
            db.session.query(ContractProjectProcess).filter(
                ContractProjectProcess.processID == processID
            ).delete(synchronize_session=False)
            db.session.commit()
            return (True, processID)
        except Exception as e:
            print e
            traceback.print_exc()
            errorInfo = ErrorInfo['TENDER_02']
            errorInfo['detail'] = str(e)
            db.session.rollback()
            return (False, errorInfo)

    def deleteContractProjectProcess(self, jsonInfo):
        userBaseManager = UserBaseManager()
        (status, info) = userBaseManager.tokenCheck(jsonInfo=jsonInfo)
        if status is not True:
            return (False, info)

        return self.__doDeleteContractProjectProcess(info=info)

    def __doGetContractProjectProcessList(self, info):
        contractID = info['contractID']
        startIndex = info['startIndex']
        pageCount = info['pageCount']

        try:
            query = db.session.query(ContractProjectProcess).filter(
                ContractProjectProcess.contractID == contractID
            )
            countQuery = db.session.query(func.count(ContractProjectProcess.processID)
                                          ).filter(
                ContractProjectProcess.contractID == contractID
            )

            allResult = query.offset(startIndex).limit(pageCount).all()
            count = countQuery.first()
            if count is None:
                count = 0
            else:
                count = count[0]

            def __generate(o):
                res = {}
                res.update(ContractProjectProcess.generate(o=o))
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

    def getContractProjectProcessList(self, jsonInfo):
        userBaseManager = UserBaseManager()
        (status, info) = userBaseManager.tokenCheck(jsonInfo=jsonInfo)
        if status is not True:
            return (False, info)

        return self.__doGetContractProjectProcessList(info=info)
