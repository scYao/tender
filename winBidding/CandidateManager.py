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
from models.Candidate import Candidate

from tool.Util import Util
from tool.config import ErrorInfo
from sqlalchemy import func


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
        candidate = Candidate(candidateID=candidateID,
                              candidateName=candidateName,
                              price=price, ranking=ranking,
                              managerName=managerName,
                              biddingID=biddingID)
        try:
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