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

from models.Type1 import Type1
from models.Type2 import Type2
from models.Type3 import Type3

class Type3Manager(Util):
    def __init__(self):
        pass

    # 后台管理, 创建一级类型
    def createType3Background(self, jsonInfo):
        info = json.loads(jsonInfo)
        tokenID = info['tokenID']
        (status, reason) = self.isTokenValid(tokenID)
        if status is not True:
            return (False, reason)

        type3Name = info['typeName']
        superTypeID = info['superTypeID']

        # type3ID = self.generateID(type3Name)
        # 获取最大ID
        maxType3IDResult = db.session.query(Type3).order_by(desc(Type3.typeID + 0)).first()
        if maxType3IDResult is None:
            maxType3ID = 0
        else:
            maxType3ID = int(maxType3IDResult.typeID)
        type3ID = maxType3ID + 1

        type3 = Type3(typeID=type3ID, typeName=type3Name, superTypeID=superTypeID)

        try:
            db.session.add(type3)
            db.session.commit()
            return (True, type3ID)
        except Exception as e:
            print e
            traceback.print_stack()
            db.session.rollback()
            errorInfo = ErrorInfo['TENDER_02']
            errorInfo['detail'] = str(e)
            return (False, errorInfo)

    def __generateType2(self, dict2, t):
        type2 = t.Type2
        if not dict2.has_key(type2.typeID):
            t2 = {}
            t2['typeID'] = type2.typeID
            t2['typeName'] = type2.typeName
            t3List = []
            dict2[type2.typeID] = t3List
            if t.Type3 is not None:
                t3 = Type3.generate(t.Type3)
                t3List.append(t3)
            t2['subTypes'] = t3List
            return t2
        else:
            if t.Type3 is not None:
                t3List = dict2[type2.typeID]
                t3 = Type3.generate(t.Type3)
                t3List.append(t3)

    def __generate(self, dict1, dict2, t):
        type1 = t.Type1
        if not dict1.has_key(type1.typeID):
            t1 = {}
            t1['typeID'] = type1.typeID
            t1['typeName'] = type1.typeName
            t2List = []
            t1['subTypes'] = t2List
            dict1[type1.typeID] = t2List
            t2 = self.__generateType2(dict2=dict2, t=t)
            if t2 is not None:
                t2List.append(t2)
            return t1
        else:
            t2List = dict1[type1.typeID]
            t2 = self.__generateType2(dict2=dict2, t=t)
            if t2 is not None:
                t2List.append(t2)

    # 获取类型列表
    def getTypeList(self):
        allResult = db.session.query(Type3, Type2, Type1).outerjoin(
            Type2, Type3.superTypeID == Type2.typeID
        ).outerjoin(
            Type1, Type2.superTypeID == Type1.typeID
        ).all()

        dict1 = {}
        dict2 = {}
        typeList = [self.__generate(dict1=dict1, dict2=dict2, t=t) for t in allResult]
        typeList = filter(None, typeList)
        return (True, typeList)

    def __generateType3(self, t):
        type3 = t
        res = {}
        res.update(Type3.generate(type3=type3))
        return res

    # 获取三级类型列表
    def getType3List(self, jsonInfo):
        info = json.loads(jsonInfo)
        typeID = info['typeID']

        allResult = db.session.query(Type3).filter(
            Type3.superTypeID == typeID
        ).all()

        typeList = [self.__generateType3(t=t) for t in allResult]
        return (True, typeList)

    def getType23ByType1(self, jsonInfo):
        info = json.loads(jsonInfo)

        typeID = info['typeID']

        allResult = db.session.query(Type2, Type3).outerjoin(
            Type3, Type3.superTypeID == Type2.typeID
        ).filter(
            Type2.superTypeID == typeID
        ).all()

        dict2 = {}
        typeList = [self.__generateType2(dict2=dict2, t=t) for t in allResult]
        typeList = filter(None, typeList)
        return (True, typeList)