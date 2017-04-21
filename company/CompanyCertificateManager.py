# coding=utf8
import sys
import traceback
import urllib2
import poster
import requests
sys.path.append("..")
import os
reload(sys)
sys.setdefaultencoding('utf-8')
import json
from sqlalchemy import desc, and_, func
from datetime import datetime
from models.flask_app import db
from models.CompanyCertificate import CompanyCertificate
from user.AdminManager import AdminManager
from models.CertificationGrade4 import CertificationGrade4


from tool.Util import Util
from tool.config import ErrorInfo

class CompanyCertificateManager(Util):

    def __init__(self):
        pass

    # 创建公司资质信息
    def createCompanyCertificate(self, jsonInfo):
        info = json.loads(jsonInfo)
        certList = info['certList']
        companyID = info['companyID']
        try:
            #判断是否已经添加
            certQuery = db.session.query(CompanyCertificate).filter(
                CompanyCertificate.companyID == companyID
            )
            certResult = certQuery.first()
            if certResult is None:
                def create(certInfo):
                    gradeType = certInfo['gradeType']
                    tag = 0 if gradeType == '主项' else 1
                    gradeName = certInfo['gradeName']
                    #判断是否存在资质信息
                    query = db.session.query(CertificationGrade4).filter(
                        CertificationGrade4.gradeName == gradeName
                    )
                    result = query.first()
                    if result is not None:
                        qualificationID = result.gradeID
                        joinID = self.generateID(qualificationID + companyID)
                        companyCertificate = CompanyCertificate(
                            joinID=joinID, companyID=companyID,
                            qualificationID=qualificationID, tag=tag
                        )
                        db.session.add(companyCertificate)
                [create(certInfo=certInfo) for certInfo in certList]
                db.session.commit()
        except Exception as e:
            db.session.rollback()
            print e
            errorInfo = ErrorInfo['TENDER_02']
            errorInfo['detail'] = str(e)
            return (False, errorInfo)
        return (True, None)

    def getCompanyCertificateList(self, jsonInfo):
        info = json.loads(jsonInfo)
        companyID = info['companyID']
        try:
            certQuery = db.session.query(
                CompanyCertificate, CertificationGrade4
            ).outerjoin(
                CertificationGrade4, CertificationGrade4.gradeID == CompanyCertificate.qualificationID
            ).filter(
                CompanyCertificate.companyID == companyID
            )
            allResult = certQuery.all()
            if allResult is None:
                return (False, ErrorInfo['TENDER_02'])
            callBackData = [self.__generateCertificate(result) for result in allResult]
            return (True, callBackData)
        except Exception as e:
            db.session.rollback()
            print e
            errorInfo = ErrorInfo['TENDER_02']
            errorInfo['detail'] = str(e)
            return (False, errorInfo)


    def __generateCertificate(self, result):
        certificationGrade4 = result.CertificationGrade4
        companyCertificate = result.CompanyCertificate
        res = {}
        res.update(CompanyCertificate.generate(c=companyCertificate))
        res.update(CertificationGrade4.generate(c=certificationGrade4))
        return res



