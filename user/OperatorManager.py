# coding=utf8
import sys
import json
sys.path.append("..")
import os, random, requests
reload(sys)
sys.setdefaultencoding('utf-8')

from datetime import datetime
from sqlalchemy import and_, text, func, desc

from models.flask_app import db
from models.Operator import Operator
from models.Message import Message
from tool.Util import Util
from tool.config import ErrorInfo


class OperatorManager(Util):
    def __init__(self):
        pass

    # 创建经办人
    def createOperator(self, jsonInfo):
        info = json.loads(jsonInfo)
        tokenID = info['tokenID']
        # 验证登录信息
        (status, userID) = self.isTokenValid(tokenID)
        if status is not True:
            return (False, userID)

        toUserID = info['userID'].replace('\'', '\\\'').replace('\"', '\\\"')
        tenderID = info['tenderID'].replace('\'', '\\\'').replace('\"', '\\\"')
        tag = info['tag'].replace('\'', '\\\'').replace('\"', '\\\"')


        operatorID = self.generateID(tenderID)

        operator = Operator(operatorID=operatorID, userID=toUserID, tenderID=tenderID, tag=tag)


        try:
            message = Message(messageID=operatorID, foreignID=tenderID,
                              fromUserID=userID, toUserID=toUserID, description='')
            db.session.add(operator)
            db.session.commit()
        except Exception as e:
            print str(e)
            # traceback.print_stack()
            db.session.rollback()
            errorInfo = ErrorInfo['TENDER_02']
            errorInfo['detail'] = str(e)
            return (False, errorInfo)
        return (True, None)