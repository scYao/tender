# -*- coding: utf-8 -*-
import os
import sys

reload(sys)
sys.setdefaultencoding('utf-8')
from flask_app import db

class Company(db.Model):
    __tablename__ = 'Company'

    companyID = db.Column(db.String(100), primary_key=True)
    companyName = db.Column(db.String(100))
    newArchiveID = db.Column(db.String(100))
    registerArea = db.Column(db.String(100))
    companyAreaType = db.Column(db.String(100))
    certificateID = db.Column(db.String(100))
    certificationAuthority = db.Column(db.String(100))
    legalRepresentative = db.Column(db.String(100))
    enterprisePrincipal = db.Column(db.String(100))
    technologyDirector = db.Column(db.String(100))
    remarks = db.Column(db.String(100))
    licenseID = db.Column(db.String(100))
    registeredCapital = db.Column(db.Float)
    companyType = db.Column(db.String(100))
    foundingTime = db.Column(db.Date)
    businessTermFrom = db.Column(db.Date)
    businessTermEnd = db.Column(db.Date)
    safetyProductionPermitID = db.Column(db.String(100))
    safePrincipal = db.Column(db.String(100))
    businessScope = db.Column(db.String(100))
    safeAuthority = db.Column(db.String(100))
    safeFromDate = db.Column(db.Date)
    safeEndDate = db.Column(db.Date)
    creditBookID = db.Column(db.String(100))
    creditScore1 = db.Column(db.Float)
    creditScore2 = db.Column(db.Float)
    creditEndDate = db.Column(db.Date)
    creditAuthority = db.Column(db.String(100))
    creditAddress = db.Column(db.String(100))
    creditWebSet = db.Column(db.String(500))
    creditContact = db.Column(db.String(100))
    creditNjAddress = db.Column(db.String(100))
    creditNjPrincipal = db.Column(db.String(100))
    creditNjTech = db.Column(db.String(100))
    creditFinancialStaff = db.Column(db.String(100))
    companyBrief = db.Column(db.Text)

    projectManager = db.relationship('ProjectManager', backref='Company', lazy='dynamic')
    companyAchievement = db.relationship('CompanyAchievement', backref='Company', lazy='dynamic')
    delinquenentConduct = db.relationship('DelinquenentConduct', backref='Company', lazy='dynamic')

    def __init__(self, companyID=None, companyName=None, newArchiveID=None,
                 registerArea=None, companyAreaType=None, certificateID=None,
                 certificationAuthority=None, legalRepresentative=None, enterprisePrincipal=None,
                 technologyDirector=None, remarks=None, licenseID=None, registeredCapital=0,
                 companyType=None, foundingTime=None, businessTermFrom=None, businessTermEnd=None,
                 safetyProductionPermitID=None, safePrincipal=None, businessScope=None,
                 safeAuthority=None, safeFromDate=None, safeEndDate=None, creditBookID=None,
                 creditScore1=0, creditScore2=0, creditEndDate=None, creditAuthority=None,
                 creditAddress=None, creditWebSet=None, creditContact=None, creditNjAddress=None,
                 creditNjPrincipal=None, creditNjTech=None, creditFinancialStaff=None, companyBrief=None):
        self.companyID = companyID
        self.companyName = companyName
        self.newArchiveID = newArchiveID
        self.registerArea = registerArea
        self.companyAreaType = companyAreaType
        self.certificateID = certificateID
        self.certificationAuthority = certificationAuthority
        self.legalRepresentative = legalRepresentative
        self.enterprisePrincipal = enterprisePrincipal
        self.technologyDirector = technologyDirector
        self.remarks = remarks
        self.licenseID = licenseID
        self.registeredCapital = registeredCapital
        self.companyType = companyType
        self.foundingTime = foundingTime
        self.businessTermFrom = businessTermFrom
        self.businessTermEnd = businessTermEnd
        self.safetyProductionPermitID = safetyProductionPermitID
        self.safePrincipal = safePrincipal
        self.businessScope = businessScope
        self.safeAuthority = safeAuthority
        self.safeFromDate = safeFromDate
        self.safeEndDate = safeEndDate
        self.creditBookID = creditBookID
        self.creditScore1 = creditScore1
        self.creditScore2 = creditScore2
        self.creditEndDate = creditEndDate
        self.creditAuthority = creditAuthority
        self.creditAddress = creditAddress
        self.creditWebSet = creditWebSet
        self.creditContact = creditContact
        self.creditNjAddress = creditNjAddress
        self.creditNjPrincipal = creditNjPrincipal
        self.creditNjTech = creditNjTech
        self.creditFinancialStaff = creditFinancialStaff
        self.companyBrief = companyBrief


    @staticmethod
    def generate(c):
        res = {}
        res['companyID'] = c.companyID
        res['companyName'] = c.companyName
        res['newArchiveID'] = c.newArchiveID
        res['registerArea'] = c.registerArea
        res['companyAreaType'] = c.companyAreaType
        res['certificateID'] = c.certificateID
        res['certificationAuthority'] = c.certificationAuthority
        res['legalRepresentative'] = c.legalRepresentative
        res['enterprisePrincipal'] = c.enterprisePrincipal
        res['technologyDirector'] = c.technologyDirector
        res['remarks'] = c.remarks
        res['licenseID'] = c.licenseID
        res['registeredCapital'] = c.registeredCapital
        res['companyType'] = c.companyType
        res['foundingTime'] = str(c.foundingTime)
        res['businessTermFrom'] = str(c.businessTermFrom)
        res['businessTermEnd'] = str(c.businessTermEnd)
        res['safetyProductionPermitID'] = c.safetyProductionPermitID
        res['safePrincipal'] = c.safePrincipal
        res['businessScope'] = c.businessScope
        res['safeAuthority'] = c.safeAuthority
        res['safeFromDate'] = str(c.safeFromDate)
        res['safeEndDate'] = str(c.safeEndDate)
        res['creditBookID'] = c.creditBookID
        res['creditScore1'] = c.creditScore1
        res['creditScore2'] = c.creditScore2
        res['creditEndDate'] = str(c.creditEndDate)
        res['creditAuthority'] = c.creditAuthority
        res['creditAddress'] = c.creditAddress
        res['creditWebSet'] = c.creditWebSet
        res['creditContact'] = c.creditContact
        res['creditNjAddress'] = c.creditNjAddress
        res['creditNjPrincipal'] = c.creditNjPrincipal
        res['creditNjTech'] = c.creditNjTech
        res['creditFinancialStaff'] = c.creditFinancialStaff
        res['companyBrief'] = c.companyBrief
        return res

    @staticmethod
    def generateBrief(c):
        res = {}
        res['companyID'] = c.companyID
        res['companyName'] = c.companyName
        return res

    def __repr__(self):
        return self.companyID
