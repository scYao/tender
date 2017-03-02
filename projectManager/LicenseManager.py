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
from models.flask_app import db
from models.ManagerLicense import ManagerLicense

from tool.Util import Util
from tool.config import ErrorInfo

class LicenseManager(Util):

    def __init__(self):
        pass

    # 创建公司
    def createManagerLicense(self, jsonInfo):
        info = json.loads(jsonInfo)
        licenseName = info['licenseName'].replace('\'', '\\\'').replace('\"', '\\\"')
        licenseNum = info['licenseNum'].replace('\'', '\\\'').replace('\"', '\\\"')
        grade = info['grade'].replace('\'', '\\\'').replace('\"', '\\\"')
        authority = info['authority'].replace('\'', '\\\'').replace('\"', '\\\"')
        licenseDate = info['licenseDate'].replace('\'', '\\\'').replace('\"', '\\\"')
        licenseEndDate = info['licenseEndDate'].replace('\'', '\\\'').replace('\"', '\\\"')
        managerID = info['managerID'].replace('\'', '\\\'').replace('\"', '\\\"')
        tag = info['tag'].replace('\'', '\\\'').replace('\"', '\\\"')

        licenseID = self.generateID(licenseName)

        managerLicense = ManagerLicense(
            licenseID=licenseID, licenseName=licenseName, licenseNum=licenseNum,
            grade=grade, authority=authority, licenseDate=licenseDate,
            licenseEndDate=licenseEndDate, managerID=managerID, tag=tag
        )
        try:
            db.session.add(managerLicense)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print e
            errorInfo = ErrorInfo['TENDER_02']
            errorInfo['detail'] = str(e)
            return (False, errorInfo)
        return (True, licenseID)
