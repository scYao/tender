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
from models.DelinquenentConduct import DelinquenentConduct

from tool.Util import Util
from tool.config import ErrorInfo

class DelinquenentConductManager(Util):

    def __init__(self):
        pass

    # 创建公司
    def createDelinquenentConduct(self, jsonInfo):
        info = json.loads(jsonInfo)
        conductName = info['conductName'].replace('\'', '\\\'').replace('\"', '\\\"')
        consequence = info['consequence'].replace('\'', '\\\'').replace('\"', '\\\"')
        penaltyType = info['penaltyType'].replace('\'', '\\\'').replace('\"', '\\\"')
        penaltyAuthority = info['penaltyAuthority'].replace('\'', '\\\'').replace('\"', '\\\"')
        penaltyDate = info['penaltyDate'].replace('\'', '\\\'').replace('\"', '\\\"')
        publicDateFrom = info['publicDateFrom'].replace('\'', '\\\'').replace('\"', '\\\"')
        publicDateEnd = info['publicDateEnd'].replace('\'', '\\\'').replace('\"', '\\\"')

        conductID = self.generateID(conductName)

        delinquenentConduct = DelinquenentConduct(
            conductID=conductID, conductName=conductName, consequence=consequence,
            penaltyType=penaltyType, penaltyAuthority=penaltyAuthority, penaltyDate=penaltyDate,
            publicDateFrom=publicDateFrom, publicDateEnd=publicDateEnd
        )
        try:
            db.session.add(delinquenentConduct)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print e
            errorInfo = ErrorInfo['TENDER_02']
            errorInfo['detail'] = str(e)
            return (False, errorInfo)
        return (True, conductID)
