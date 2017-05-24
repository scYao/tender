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
from models.ContractEmergency import ContractEmergency
from tool.Util import Util
from tool.config import ErrorInfo
from user.UserBaseManager import UserBaseManager

class ContractEmergencyManager(Util):
    def __init__(self):
        pass


    def __doCreateContractEmergency(self, info):
        createTime = info['createTime']
        description = info['description']
        resolvent = info['resolvent']
        contractID = info['contractID'].replace('\'', '\\\'').replace('\"', '\\\"')

        emergencyID = self.generateID(contractID)

        try:
            contractEmergency = ContractEmergency(emergencyID=emergencyID,
                                                  createTime=createTime,
                                                  description=description,
                                                  resolvent=resolvent, contractID=contractID)
            db.session.add(contractEmergency)
            db.session.commit(contractEmergency)
            return (True, emergencyID)
        except Exception as e:
            print e
            traceback.print_exc()
            errorInfo = ErrorInfo['TENDER_02']
            errorInfo['detail'] = str(e)
            db.session.rollback()
            return (False, errorInfo)

    # 创建突发事件
    def createContractEmergency(self, jsonInfo):
        userBaseManager = UserBaseManager()
        (status, info) = userBaseManager.tokenCheck(jsonInfo=jsonInfo)
        if status is not True:
            return (False, info)

        return self.__doCreateContractEmergency(info=info)

    def __doDeleteContractEmergency(self, info):
        emergencyID = info['emergencyID']
        try:
            db.session.query(ContractEmergency).filter(
                ContractEmergency.emergencyID == emergencyID
            ).delete(synchronize_session=False)
            db.session.commit()
            return (True, emergencyID)
        except Exception as e:
            print e
            traceback.print_exc()
            errorInfo = ErrorInfo['TENDER_02']
            errorInfo['detail'] = str(e)
            db.session.rollback()
            return (False, errorInfo)

    # 删除突发事件
    def deleteContractEmergency(self, jsonInfo):
        userBaseManager = UserBaseManager()
        (status, info) = userBaseManager.tokenCheck(jsonInfo=jsonInfo)
        if status is not True:
            return (False, info)

        return self.__doDeleteContractEmergency(info=info)

    def __doGetContractEmergencyList(self, info):
        contractID = info['contractID']
        startIndex = info['startIndex']
        pageCount = info['pageCount']

        try:
            query = db.session.query(ContractEmergency).filter(
                ContractEmergency.contractID == contractID
            )
            countQuery = db.session.query(func.count(ContractEmergency)
                                          ).filter(
                ContractEmergency.contractID == contractID
            )
            allResult = query.offset(startIndex).limit(pageCount).all()
            count = countQuery.first()
            if count is None:
                count = 0
            else:
                count = count[0]

            def __generate(o):
                res = {}
                res.update(ContractEmergency.generate(o=o))
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

    # 获取突发事件列表
    def getContractEmergencyList(self, jsonInfo):
        userBaseManager = UserBaseManager()
        (status, info) = userBaseManager.tokenCheck(jsonInfo=jsonInfo)
        if status is not True:
            return (False, info)

        return self.__doGetContractEmergencyList(info=info)