# coding=utf8
import sys
import traceback
import urllib2
import poster
import requests
from sqlalchemy import desc

sys.path.append("..")
import os
reload(sys)
sys.setdefaultencoding('utf-8')
import json
from datetime import datetime
from sqlalchemy import desc, and_
from models.flask_app import db, cache
from models.CompanyAssistant import CompanyAssistant

from tool.Util import Util
from tool.config import ErrorInfo
from image.ImageManager import ImageManager
from user.AdminManager import AdminManager

from sqlalchemy import func


class CompanyAssistantManager(Util):

    def __init__(self):
        pass

    def create(self, jsonInfo):
        info = json.loads(jsonInfo)
        companyName = info['companyName'].replace('\'', '\\\'').replace('\"', '\\\"')
        foreignCompanyID = info['foreignCompanyID'].replace('\'', '\\\'').replace('\"', '\\\"')

        (status, reason) = self.doesCompanyExists(info=info)
        if status is True:
            return (False, reason)

        companyID = self.generateID(companyName)
        companyAssistant = CompanyAssistant(companyID=companyID, companyName=companyName,
                                            foreignCompanyID=foreignCompanyID)

        try:
            db.session.add(companyAssistant)
            db.session.commit()
        except Exception as e:
            print str(e)
            # traceback.print_stack()
            db.session.rollback()
            errorInfo = ErrorInfo['TENDER_02']
            errorInfo['detail'] = str(e)
            return (False, errorInfo)
        return (True, companyID)

    def doesCompanyExists(self, info):
        companyName = info['companyName']
        try:
            result = db.session.query(CompanyAssistant).filter(
                CompanyAssistant.companyName == companyName
            ).first()

            if result is not None:
                return (True, result.companyID)
            else:
                return (False, None)
        except Exception as e:
            print str(e)
            # traceback.print_stack()
            db.session.rollback()
            errorInfo = ErrorInfo['TENDER_02']
            errorInfo['detail'] = str(e)
            return (False, errorInfo)


    def getCompanyAssistantListBackground(self, jsonInfo):
        info = json.loads(jsonInfo)
        startIndex = info['startIndex']
        pageCount = info['pageCount']
        # 管理员身份校验, 里面已经校验过token合法性
        adminManager = AdminManager()
        (status, reason) = adminManager.adminAuth(jsonInfo)
        if status is not True:
            return (False, reason)

        try:
            query = db.session.query(CompanyAssistant).offset(startIndex).limit(pageCount)
            allResult = query.all()
            companyList = [CompanyAssistant.generate(o=c) for c in allResult]
            count = db.session.query(func.count(CompanyAssistant.companyID)).first()
            companyResult = {}
            companyResult['companyList'] = companyList
            companyResult['count'] = count
            return (True, companyResult)
        except Exception as e:
            print str(e)
            # traceback.print_stack()
            db.session.rollback()
            errorInfo = ErrorInfo['TENDER_02']
            errorInfo['detail'] = str(e)
            return (False, errorInfo)

    def getCompanyAssistantIDByName(self, info):
        companyName = info['companyName']

        try:
            result = db.session.query(CompanyAssistant).filter(
                CompanyAssistant.companyName == companyName
            ).first()
            if result is None:
                return (False, None)
            return (True, result.companyID)
        except Exception as e:
            print e
            errorInfo = ErrorInfo['TENDER_02']
            errorInfo['detail'] = str(e)
            db.session.rollback()
            return (False, errorInfo)