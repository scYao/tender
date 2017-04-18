# coding=utf8
import sys
import json
from tender.CustomizedTenderManager import CustomizedTenderManager

from user.UserManager import UserManager

sys.path.append("..")
import os, random, requests
reload(sys)
sys.setdefaultencoding('utf-8')

from datetime import datetime
from sqlalchemy import and_, text, func, desc

from models.flask_app import db
from models.UserInfo import UserInfo
from tool.Util import Util
from tool.config import ErrorInfo
from tool.tagconfig import OPERATOR_TAG_CREATED, DOING_STEP, DONE_STEP, HISTORY_STEP, PUSH_TENDER_INFO_TAG_CUS, \
    PUSH_TENDER_INFO_TAG_TENDER
from tool.tagconfig import USER_TAG_OPERATOR, USER_TAG_RESPONSIBLEPERSON, USER_TAG_AUDITOR, USER_TAG_BOSS
from pushedTender.TenderCommentManager import TenderCommentManager

from UserManager import UserManager


class UserBaseManager(Util):

    def __init__(self):
        pass

    def addPushedDataInfoToUser(self, o, pushedTenderManager, info):
        info['userID'] = o['userID']
        info['userType'] = o['userType']
        (status, dataInfo) = pushedTenderManager.getDataInfoByUserID(info=info)
        o.update(dataInfo)
        return None

    def getUserInfoByUserID(self, jsonInfo):
        info = json.loads(jsonInfo)
        tokenID = info['tokenID']
        (status, userID) = self.isTokenValid(tokenID)
        if status is not True:
            errorInfo = ErrorInfo['TENDER_01']
            return (False, errorInfo)

        info['userID'] = userID
        return self.getUserInfo(info=info)

    def getUserInfo(self, info):
        userManager = UserManager()
        return userManager.getUserInfo(info=info)
