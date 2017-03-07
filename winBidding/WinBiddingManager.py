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
from models.WinBiddingPub import WinBiddingPub

from tool.Util import Util
from tool.config import ErrorInfo
from sqlalchemy import func


class WinBiddingManager(Util):

    def __init__(self):
        pass

    # 创建中标公示
    def createWinBidding(self, jsonInfo):
        info = json.loads(jsonInfo)
        title = info['title'].replace('\'', '\\\'').replace('\"', '\\\"')
        publicDate = info['publicDate'].replace('\'', '\\\'').replace('\"', '\\\"')
        biddingNum = info['biddingNum'].replace('\'', '\\\'').replace('\"', '\\\"')

        biddingID = self.generateID(biddingNum)

        winBidding = WinBiddingPub(biddingID=biddingID, title=title, publicDate=publicDate, biddingNum=biddingNum)

        try:
            db.session.add(winBidding)
            db.session.commit()
        except Exception as e:
            # traceback.print_stack()
            db.session.rollback()
            print e
            errorInfo = ErrorInfo['TENDER_02']
            errorInfo['detail'] = str(e)
            return (False, errorInfo)
        return (True, biddingID)