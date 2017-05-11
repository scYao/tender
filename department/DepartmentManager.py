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
from models.Department import Department
from datetime import datetime

from tool.Util import Util
from tool.config import ErrorInfo
from department.DepartmentAreaManager import DepartmentAreaManager

from sqlalchemy import func


class DepartmentManager(Util):
    def __init__(self):
        pass

    # 创建部门
    def createDepartment(self, info):
        departmentName = info['departmentName']

        departmentID = self.generateID(departmentName)
        now = datetime.now()
        try:
            department = Department(departmentID=departmentID,
                                    departmentName=departmentName, createTime=now)
            db.session.add(department)
            db.session.commit()
            return (True, departmentID)
        except Exception as e:
            print e
            traceback.print_exc()
            errorInfo = ErrorInfo['TENDER_02']
            errorInfo['detail'] = str(e)
            db.session.rollback()
            return (False, errorInfo)

    # 修改部门名称
    def updateDepartmentName(self, info):
        departmentName = info['departmentName']
        departmentID = info['departmentID']
        try:
            db.session.query(Department).filter(
                Department.departmentID == departmentID
            ).update({
                Department.departmentName : departmentName
            }, synchronize_session=False)
            db.session.commit()

            return (True, departmentID)
        except Exception as e:
            print e
            traceback.print_exc()
            errorInfo = ErrorInfo['TENDER_02']
            errorInfo['detail'] = str(e)
            db.session.rollback()
            return (False, errorInfo)

    # 删除部门
    def deleteDepartment(self, info):
        departmentID = info['departmentID']
        try:
            areaManager = DepartmentAreaManager()
            (status, reason) = areaManager.deleteAreaByDepartmentID(info=info)
            if status is not True:
                return (False, reason)
            db.session.query(Department).filter(
                Department.departmentID == departmentID
            ).delete(synchronize_session=False)
            db.session.commit()
            return (True, departmentID)
        except Exception as e:
            print e
            traceback.print_exc()
            errorInfo = ErrorInfo['TENDER_02']
            errorInfo['detail'] = str(e)
            db.session.rollback()
            return (False, errorInfo)

    def __generateDepartment(self, o):
        res = {}
        res.update(Department.generate(o=o))
        return res

    #
    def getDepartmentList(self, info):
        startIndex = info['startIndex']
        pageCount = info['pageCount']
        try:
            query = db.session.query(Department)
            query = query.offset(startIndex).limit(pageCount)
            allResult = query.all()

            countQuery = db.session.query(func.count(Department.departmentID))

            dataList = [self.__generateDepartment(o=o) for o in allResult]
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

    def getDepartmentByID(self, info):
        departmentID = info['departmentID']
        try:
            query = db.session.query(Department).filter(
                Department.departmentID == departmentID
            )
            result = query.first()
            dataResult = {}
            dataResult.update(Department.generate(o=result))
            return (True, dataResult)

        except Exception as e:
            print e
            traceback.print_exc()
            errorInfo = ErrorInfo['TENDER_02']
            errorInfo['detail'] = str(e)
            db.session.rollback()
            return (False, errorInfo)