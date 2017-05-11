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
from models.DepartmentArea import DepartmentArea
from datetime import datetime

from tool.Util import Util
from tool.config import ErrorInfo
from tool.tagconfig import FAVORITE_TAG_TENDER, FAVORITE_TAG_WIN_BIDDING

from sqlalchemy import func


class DepartmentAreaManager(Util):
    def __init__(self):
        pass

    # 创建部门区域
    def createDepartmentArea(self, info):
        departmentID = info['departmentID']
        areaName = info['areaName']

        try:
            now = datetime.now()
            areaID = self.generateID(areaName)
            departmentArea = DepartmentArea(areaID=areaID, areaName=areaName,
                                            createTime=now, departmentID=departmentID)
            db.session.add(departmentArea)
            db.session.commit()
            return (True, areaID)
        except Exception as e:
            print e
            traceback.print_exc()
            errorInfo = ErrorInfo['TENDER_02']
            errorInfo['detail'] = str(e)
            db.session.rollback()
            return (False, errorInfo)

    # 更改部门名称
    def updateDepartmentAreaName(self, info):
        areaID = info['areaID']
        areaName = info['areaName']
        try:
            db.session.query(DepartmentArea).filter(
                DepartmentArea.areaID == areaID
            ).update({
                DepartmentArea.areaName : areaName
            }, synchronize_session=False)
            db.session.commit()
            return (True, areaID)
        except Exception as e:
            print e
            traceback.print_exc()
            errorInfo = ErrorInfo['TENDER_02']
            errorInfo['detail'] = str(e)
            db.session.rollback()
            return (False, errorInfo)

    #  删除部门区域
    def deleteDepartmentArea(self, info):
        areaID = info['areaID']
        try:
            db.session.query(DepartmentArea).filter(
                DepartmentArea.areaID == areaID
            ).delete(synchronize_session=False)
            db.session.commit()
            return (True, areaID)
        except Exception as e:
            print e
            traceback.print_exc()
            errorInfo = ErrorInfo['TENDER_02']
            errorInfo['detail'] = str(e)
            db.session.rollback()
            return (False, errorInfo)

    def deleteAreaByDepartmentID(self, info):
        departmentID = info['departmentID']
        try:
            db.session.query(DepartmentArea).filter(
                DepartmentArea.departmentID == departmentID
            ).delete(synchronize_session=False)
            db.session.commit()
            return (True, None)
        except Exception as e:
            print e
            traceback.print_exc()
            errorInfo = ErrorInfo['TENDER_02']
            errorInfo['detail'] = str(e)
            db.session.rollback()
            return (False, errorInfo)

    def __generateArea(self, o):
        res = {}
        res.update(DepartmentArea.generate(o=o))
        return res

    #  获取去也列表
    def getAreaListByDepartmentID(self, info):
        departmentID = info['departmentID']
        startIndex = info['startIndex']
        pageCount = info['pageCount']
        try:
            query = db.session.query(DepartmentArea).filter(
                DepartmentArea.departmentID == departmentID
            )
            countQuery = db.session.query(func.count(DepartmentArea.areaID)).filter(
                DepartmentArea.departmentID == departmentID
            )
            query = query.offset(startIndex).limit(pageCount)
            allResult = query.all()

            dataList = [self.__generateArea(o=o) for o in allResult]
            count = countQuery.first()
            if count is None:
                count = 0
            else:
                count = count[0]
            dataResult = {}
            dataResult['dataList'] = dataList
            dataResult['count'] = count
            return (True, dataResult)
        except Exception as e:
            print e
            traceback.print_exc()
            errorInfo = ErrorInfo['TENDER_02']
            errorInfo['detail'] = str(e)
            db.session.rollback()
            return (False, errorInfo)