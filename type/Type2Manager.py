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
from models.flask_app import db
from datetime import datetime

from tool.Util import Util
from tool.config import ErrorInfo

from models.Type2 import Type2

class Type2Manager(Util):
    def __init__(self):
        pass

    # 后台管理, 创建一级类型
    def createType2Background(self, jsonInfo):
        info = json.loads(jsonInfo)
        tokenID = info['tokenID']
        (status, reason) = self.isTokenValid(tokenID)
        if status is not True:
            return (False, reason)

        type2Name = info['typeName']
        superTypeID = info['superTypeID']

        # type2ID = self.generateID(type2Name)
        # 获取最大ID
        maxType2IDResult = db.session.query(Type2).order_by(desc(Type2.typeID + 0)).first()
        if maxType2IDResult is None:
            maxType2ID = 0
        else:
            maxType2ID = int(maxType2IDResult.typeID)
        type2ID = maxType2ID + 1

        type2 = Type2(typeID=type2ID, typeName=type2Name, superTypeID=superTypeID)

        try:
            db.session.add(type2)
            db.session.commit()
            return (True, type2ID)
        except Exception as e:
            print e
            traceback.print_stack()
            db.session.rollback()
            errorInfo = ErrorInfo['TENDER_02']
            errorInfo['detail'] = str(e)
            return (False, errorInfo)

    def __generate(self, t):
        type2 = t
        res = {}
        res.update(Type2.generate(type2=type2))
        return res

    # 获取二级类型列表
    def getType2List(self, jsonInfo):
        info = json.loads(jsonInfo)
        typeID = info['typeID']

        allResult = db.session.query(Type2).filter(
            Type2.superTypeID == typeID
        ).all()

        typeList = [self.__generate(t=t) for t in allResult]
        return (True, typeList)
