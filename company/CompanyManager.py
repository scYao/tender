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
from models.flask_app import db, cache
from models.DelinquenentConduct import DelinquenentConduct
from models.Company import Company
from models.ImgPath import ImgPath

from tool.Util import Util
from tool.config import ErrorInfo
from image.ImageManager import ImageManager

from sqlalchemy import func


class CompanyManager(Util):

    def __init__(self):
        pass

    # 创建公司
    def createCompany(self, jsonInfo):
        info = json.loads(jsonInfo)
        companyName = info['companyName'].replace('\'', '\\\'').replace('\"', '\\\"')
        newArchiveID = info['newArchiveID'].replace('\'', '\\\'').replace('\"', '\\\"')
        registerArea = info['registerArea'].replace('\'', '\\\'').replace('\"', '\\\"')
        companyAreaType = info['companyAreaType'].replace('\'', '\\\'').replace('\"', '\\\"')
        certificateID = info['certificateID'].replace('\'', '\\\'').replace('\"', '\\\"')
        certificationAuthority = info['certificationAuthority'].replace('\'', '\\\'').replace('\"', '\\\"')
        legalRepresentative = info['legalRepresentative'].replace('\'', '\\\'').replace('\"', '\\\"')
        enterprisePrincipal = info['enterprisePrincipal'].replace('\'', '\\\'').replace('\"', '\\\"')
        technologyDirector = info['technologyDirector'].replace('\'', '\\\'').replace('\"', '\\\"')
        remarks = info['remarks'].replace('\'', '\\\'').replace('\"', '\\\"')
        licenseID = info['licenseID'].replace('\'', '\\\'').replace('\"', '\\\"')
        registeredCapital = info['registeredCapital'].replace('\'', '\\\'').replace('\"', '\\\"')
        companyType = info['companyType'].replace('\'', '\\\'').replace('\"', '\\\"')
        foundingTime = info['foundingTime'].replace('\'', '\\\'').replace('\"', '\\\"')
        businessTermFrom = info['businessTermFrom'].replace('\'', '\\\'').replace('\"', '\\\"')
        safetyProductionPermitID = info['safetyProductionPermitID'].replace('\'', '\\\'').replace('\"', '\\\"')
        safePrincipal = info['safePrincipal'].replace('\'', '\\\'').replace('\"', '\\\"')
        businessScope = info['businessScope'].replace('\'', '\\\'').replace('\"', '\\\"')
        safeAuthority = info['safeAuthority'].replace('\'', '\\\'').replace('\"', '\\\"')
        safeFromDate = info['safeFromDate'].replace('\'', '\\\'').replace('\"', '\\\"')
        safeEndDate = info['safeEndDate'].replace('\'', '\\\'').replace('\"', '\\\"')
        creditBookID = info['creditBookID'].replace('\'', '\\\'').replace('\"', '\\\"')
        creditScore1 = info['creditScore1'].replace('\'', '\\\'').replace('\"', '\\\"')
        creditScore2 = info['creditScore2'].replace('\'', '\\\'').replace('\"', '\\\"')
        creditEndDate = info['creditEndDate'].replace('\'', '\\\'').replace('\"', '\\\"')
        creditAuthority = info['creditAuthority'].replace('\'', '\\\'').replace('\"', '\\\"')
        creditAddress = info['creditAddress'].replace('\'', '\\\'').replace('\"', '\\\"')
        creditWebSet = info['creditWebSet'].replace('\'', '\\\'').replace('\"', '\\\"')
        creditContact = info['creditContact'].replace('\'', '\\\'').replace('\"', '\\\"')
        creditNjAddress = info['creditNjAddress'].replace('\'', '\\\'').replace('\"', '\\\"')
        creditNjPrincipal = info['creditNjPrincipal'].replace('\'', '\\\'').replace('\"', '\\\"')
        creditNjTech = info['creditNjTech'].replace('\'', '\\\'').replace('\"', '\\\"')
        creditFinancialStaff = info['creditFinancialStaff'].replace('\'', '\\\'').replace('\"', '\\\"')
        companyBrief = info['companyBrief'].replace('\'', '\\\'').replace('\"', '\\\"')

        companyID = self.generateID(companyName)

        company = Company(companyID=companyID, companyName=companyName, newArchiveID=newArchiveID,
                          registerArea=registerArea, companyAreaType=companyAreaType,
                          certificateID=certificateID, certificationAuthority=certificationAuthority,
                          legalRepresentative=legalRepresentative, enterprisePrincipal=enterprisePrincipal,
                          technologyDirector=technologyDirector, remarks=remarks, licenseID=licenseID,
                          registeredCapital=registeredCapital, companyType=companyType, foundingTime=foundingTime,
                          businessTermFrom=businessTermFrom, safetyProductionPermitID=safetyProductionPermitID,
                          safePrincipal=safePrincipal, businessScope=businessScope, safeAuthority=safeAuthority,
                          safeFromDate=safeFromDate, safeEndDate=safeEndDate, creditBookID=creditBookID,
                          creditScore1=creditScore1, creditScore2=creditScore2, creditEndDate=creditEndDate,
                          creditAuthority=creditAuthority, creditAddress=creditAddress, creditWebSet=creditWebSet,
                          creditContact=creditContact, creditNjAddress=creditNjAddress, creditNjPrincipal=creditNjPrincipal,
                          creditNjTech=creditNjTech, creditFinancialStaff=creditFinancialStaff, companyBrief=companyBrief)
        try:
            db.session.add(company)
            db.session.commit()
        except Exception as e:
            # traceback.print_stack()
            db.session.rollback()
            print e
            errorInfo = ErrorInfo['TENDER_02']
            errorInfo['detail'] = str(e)
            return (False, errorInfo)
        return (True, companyID)

    def uploadCompanyImage(self, jsonInfo):
        info = json.loads(jsonInfo)
        imageManager = ImageManager()
        try:
            imageManager.addImage(info=info)
            db.session.commit()
        except Exception as e:
            # traceback.print_stack()
            db.session.rollback()
            print e
            errorInfo = ErrorInfo['TENDER_02']
            errorInfo['detail'] = str(e)
            return (False, errorInfo)
        return (True, None)

    # 获取公司列表,后台管理
    @cache.memoize(timeout=60 * 2)
    def getCompanyListBackground(self, jsonInfo):
        info = json.loads(jsonInfo)
        startIndex = info['startIndex']
        pageCount = info['pageCount']
        tokenID = info['tokenID']
        (status, userID) = self.isTokenValid(tokenID)
        if not status:
            errorInfo = ErrorInfo['TENDER_01']
            return (False, errorInfo)
        # 获取tenderID列表
        query = self.__getQueryResult(info)
        allResult = query.offset(startIndex).limit(pageCount).all()
        companyList = [Company.generateBrief(result) for result in allResult]
        return (True, companyList)

    def __getQueryResult(self, info):
        query = db.session.query(Company)
        return query

    def __generateCompanyDetail(self, allResult):
        ossInfo = {}
        ossInfo['bucket'] = 'sjtender'
        directory = 'company'
        res = {}
        imgInfo = {'imgPathList': []}
        for result in allResult:
            company = result.Company
            img = result.ImgPath

            res.update(Company.generate(company))
            imgInfo['imgPathList'].append(ImgPath.generate(img, ossInfo, directory))
        res.update(imgInfo)
        return res

    def __getDetailQueryResult(self, info):
        companyID = info['companyID']
        query = db.session.query(
            Company, ImgPath
        ).outerjoin(
          ImgPath, Company.companyID == ImgPath.foreignID
        ).filter(
            Company.companyID == companyID
        )
        return query

    #获取企业信息详情，后台
    def getCompanyDetailBackground(self, jsonInfo):
        info = json.loads(jsonInfo)
        tokenID = info['tokenID']
        (status, userID) = self.isTokenValid(tokenID)
        if not status:
            errorInfo = ErrorInfo['TENDER_01']
            return (False, errorInfo)
        query = self.__getDetailQueryResult(info)
        allResult = query.all()
        companyDetail = self.__generateCompanyDetail(allResult)
        return (True, companyDetail)
