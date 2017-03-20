# coding=utf8
import sys
import traceback
import urllib2
import poster
import requests
from sqlalchemy import desc

from user.AdminManager import AdminManager

sys.path.append("..")
import os
reload(sys)
sys.setdefaultencoding('utf-8')
import json
from datetime import datetime
from models.flask_app import db
from models.DelinquenentConduct import DelinquenentConduct
from models.Company import Company

from tool.Util import Util
from tool.config import ErrorInfo
from models.CertificationGrade4 import CertificationGrade4

from sqlalchemy import func


class CertificationGrade4Manager(Util):

    def __init__(self):
        pass

    # 创建一级资质等级
    def createCertificationGrade4(self, jsonInfo):
        info = json.loads(jsonInfo)
        gradeName = info['gradeName'].replace('\'', '\\\'').replace('\"', '\\\"')
        superiorID = info['superiorID'].replace('\'', '\\\'').replace('\"', '\\\"')

        gradeID = self.generateID(gradeName)

        certificationGrade4 = CertificationGrade4(gradeID=gradeID, gradeName=gradeName, superiorID=superiorID)
        try:
            db.session.add(certificationGrade4)
            db.session.commit()
        except Exception as e:
            # traceback.print_stack()
            db.session.rollback()
            print e
            errorInfo = ErrorInfo['TENDER_02']
            errorInfo['detail'] = str(e)
            return (False, errorInfo)
        return (True, gradeID)

    def getGrade4ListBackground(self, jsonInfo):
        # 管理员身份校验, 里面已经校验过token合法性
        adminManager = AdminManager()
        (status, reason) = adminManager.adminAuth(jsonInfo)
        if status is not True:
            return (False, reason)
        return self.getGrade4List(jsonInfo=jsonInfo)

    def getGrade4List(self, jsonInfo):
        info = json.loads(jsonInfo)
        gradeID = info['gradeID']
        # 获取tenderID列表
        try:
            query = db.session.query(CertificationGrade4).filter(
                CertificationGrade4.superiorID == gradeID
            )
            allResult = query.all()
            callBackInfo = [CertificationGrade4.generate(result) for result in allResult]
            return (True, callBackInfo)
        except Exception as e:
            print e
            errorInfo = ErrorInfo['TENDER_02']
            errorInfo['detail'] = str(e)
            db.session.rollback()
            return (False, errorInfo)