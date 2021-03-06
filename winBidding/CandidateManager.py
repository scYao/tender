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
from datetime import datetime
from sqlalchemy import desc, and_
from models.flask_app import db
from models.Candidate import Candidate
from models.CompanyAssistant import CompanyAssistant

from tool.Util import Util
from tool.config import ErrorInfo
from sqlalchemy import func
from company.CompanyManager import CompanyManager
from company.CompanyAssistantManager import CompanyAssistantManager

class CandidateManager(Util):

    def __init__(self):
        pass

    # 创建中标公示
    def createCandidate(self, jsonInfo):
        info = json.loads(jsonInfo)
        # candidateID = info['candidateID'].replace('\'', '\\\'').replace('\"', '\\\"')
        candidateName = info['candidateName'].replace('\'', '\\\'').replace('\"', '\\\"')
        # companyID = info['companyID'].replace('\'', '\\\'').replace('\"', '\\\"')
        price = info['price']
        ranking = info['ranking']
        managerName = info['managerName'].replace('\'', '\\\'').replace('\"', '\\\"')
        # managerID = info['managerID'].replace('\'', '\\\'').replace('\"', '\\\"')
        biddingID = info['biddingID'].replace('\'', '\\\'').replace('\"', '\\\"')

        candidateID = self.generateID(candidateName)
        _companyID = '-1'

        companyAssistantManager = CompanyAssistantManager()
        info['companyName'] = candidateName.strip()
        (status, companyID) = companyAssistantManager.getCompanyAssistantIDByName(info=info)
        if status is True:
            _companyID = companyID

        (status, reason) = self.doesCandidateExists(info=info)
        if status is True:
            return (False, ErrorInfo['TENDER_16'])
        try:
            info['companyName'] = candidateName.strip()
            if _companyID == '-1':
                (status, _companyID) = self.createCompanyAssistant(info=info)
            candidate = Candidate(candidateID=candidateID,
                                  candidateName=candidateName,
                                  price=price, ranking=ranking,
                                  managerName=managerName,
                                  biddingID=biddingID, companyID=_companyID)
            db.session.add(candidate)
            db.session.commit()
        except Exception as e:
            # traceback.print_stack()
            db.session.rollback()
            print e
            errorInfo = ErrorInfo['TENDER_02']
            errorInfo['detail'] = str(e)
            return (False, errorInfo)
        return (True, biddingID)

    def createCompanyAssistant(self, info):
        companyName = info['companyName']
        companyManager = CompanyManager()
        (status, _companyID) = companyManager.getCompanyIDByName(info=info)
        if status is False:
            _companyID = '-1'
            companyID = self.generateID(companyName)
        else:
            companyID = _companyID
        companyAssistant = CompanyAssistant(companyID=companyID, companyName=companyName, foreignCompanyID=_companyID)
        db.session.add(companyAssistant)
        return (True, None)

    # 通过title判断改标段是否存在, 存在为True
    def doesCandidateExists(self, info):
        candidateName = info['candidateName']
        biddingID = info['biddingID']
        try:
            result = db.session.query(Candidate).filter(
                and_(Candidate.candidateName == candidateName,
                     Candidate.biddingID == biddingID)
            ).first()
            if result is not None:
                return (True, result.candidateID)
            else:
                return (False, None)
        except Exception as e:
            print str(e)
            # traceback.print_stack()
            db.session.rollback()
            errorInfo = ErrorInfo['TENDER_02']
            errorInfo['detail'] = str(e)
            return (False, errorInfo)