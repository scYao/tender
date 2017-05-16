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
from sqlalchemy import and_
from models.flask_app import db
from models.DepartmentRight import DepartmentRight
from datetime import datetime

from tool.Util import Util
from tool.config import ErrorInfo

from sqlalchemy import func


class DepartmentRightManager(Util):
    def __init__(self):
        pass

    # 设置权限
    def createRight(self, info):
        areaID = info['areaID']
        userID = info['userID']
        tag = info['tag']

        try:
            rightID = self.generateID(areaID + userID)
            result = db.session.query(DepartmentRight).filter(and_(
                DepartmentRight.areaID == areaID,
                DepartmentRight.userID == userID
            )).first()
            if result is not None:
                return (False, ErrorInfo['TENDER_44'])
            departmentRight = DepartmentRight(rightID=rightID,
                                areaID=areaID, userID=userID, tag=tag)
            db.session.add(departmentRight)
            db.session.commit()
            return (True, rightID)
        except Exception as e:
            print e
            traceback.print_exc()
            errorInfo = ErrorInfo['TENDER_02']
            errorInfo['detail'] = str(e)
            db.session.rollback()
            return (False, errorInfo)


    def deleteRight(self, info):
        rightID = info['rightID']
        try:
            db.session.query(DepartmentRight).filter(
                DepartmentRight.rightID == rightID
            ).delete(synchronize_session=False)
            db.session.commit()
            return (True, rightID)
        except Exception as e:
            print e
            traceback.print_exc()
            errorInfo = ErrorInfo['TENDER_02']
            errorInfo['detail'] = str(e)
            db.session.rollback()
            return (False, errorInfo)

    def getRightDicByUserID(self, info):
        userID = info['userID']
        try:
            allResult = db.session.query(DepartmentRight).filter(
                DepartmentRight.userID == userID
            ).all()

            def generateRightDic(o, rightDic):
                rightDic[o.areaID] = o.rightID

            rightDic = {}

            _ = [generateRightDic(o=o, rightDic=rightDic) for o in allResult]
            return (True, rightDic)
        except Exception as e:
            print e
            traceback.print_exc()
            errorInfo = ErrorInfo['TENDER_02']
            errorInfo['detail'] = str(e)
            db.session.rollback()
            return (False, errorInfo)

    #  获取用户拥有的区域列表
    def getAreaListByUserID(self, info):
        userID = info['userID']
        try:
            allResult = db.session.query(DepartmentRight).filter(
                DepartmentRight.userID == userID
            ).all()

            dataList = [o.areaID for o in allResult]
            return (True, dataList)
        except Exception as e:
            print e
            traceback.print_exc()
            errorInfo = ErrorInfo['TENDER_02']
            errorInfo['detail'] = str(e)
            db.session.rollback()
            return (False, errorInfo)