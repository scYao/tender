# coding=utf8
import sys
import traceback
import urllib2
import poster
import requests
from sqlalchemy import desc
from tool.tagconfig import USER_TAG_RESPONSIBLEPERSON, PUSH_TENDER_INFO_TAG_STATE_APPROVE, \
    PUSH_TENDER_INFO_TAG_STEP_WAIT, PUSH_TENDER_INFO_TAG_STEP_DOING, OPERATOR_TAG_YES
from tool.Util import Util
from tool.config import ErrorInfo

sys.path.append("..")
import os
reload(sys)
sys.setdefaultencoding('utf-8')
import json
from datetime import datetime
from sqlalchemy import func, desc, and_, or_
from tool.tagconfig import USER_TAG_OPERATOR, USER_TAG_RESPONSIBLEPERSON, USER_TAG_AUDITOR, USER_TAG_BOSS
from tool.tagconfig import OPERATOR_TAG_CREATED, DOING_STEP, DONE_STEP, HISTORY_STEP

from models.flask_app import db
from models.PushedTenderInfo import PushedTenderInfo
from models.UserInfo import UserInfo
from models.Tender import Tender
from models.Operator import Operator
from models.Token import Token
from models.TenderComment import TenderComment
from PushedTenderManager import PushedTenderManager

class TenderCommentManager(Util):

    def __init__(self):
        pass

    # 审定人批注正在进行中的项目
    def createTenderComment(self, info):
        userID = info['userID']
        tenderID = info['tenderID']
        commentID = self.generateID(userID + tenderID)
        createTime = datetime.now()
        commentInfo = {}
        commentInfo['userID'] = userID
        commentInfo['createTime'] = createTime
        commentInfo['tenderID'] = tenderID
        commentInfo['commentID'] = commentID
        commentInfo['description'] = info['description'].replace('\'', '\\\'').replace('\"', '\\\"')
        try:
            TenderComment.create(info=commentInfo)
            db.session.commit()
            return (True, None)
        except Exception as e:
            print e
            errorInfo = ErrorInfo['TENDER_02']
            errorInfo['detail'] = str(e)
            db.session.rollback()
            return (False, errorInfo)


    #删除批注
    def deleteTenderComment(self, info):
        userID = info['userID']
        commentID = info['commentID']
        try:
            query = db.session.query(TenderComment).filter(
                and_(
                    TenderComment.userID == userID,
                    TenderComment.commentID == commentID
                )
            )
            query.delete(synchronize_session=False)
            db.session.commit()
            return (True, None)
        except Exception as e:
            print e
            errorInfo = ErrorInfo['TENDER_02']
            errorInfo['detail'] = str(e)
            db.session.rollback()
            return (False, errorInfo)

    def getCommentList(self, info):
        pushedID = info['pushedID']

        db.session.query(TenderComment).filter(
            TenderComment.pushedID == pushedID
        ).all()