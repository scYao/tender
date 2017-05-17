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
from models.DepartmentArea import DepartmentArea
from models.DepartmentRight import DepartmentRight
from datetime import datetime

from tool.Util import Util
from tool.config import ErrorInfo
from tool.tagconfig import FAVORITE_TAG_TENDER, FAVORITE_TAG_WIN_BIDDING, USER_TAG_BOSS

from department.DepartmentRightManager import DepartmentRightManager
from user.UserBaseManager import UserBaseManager

from sqlalchemy import func


class DepartmentAreaManager(Util):
    def __init__(self):
        pass

    # 创建部门区域
    def createDepartmentArea(self, info):
        departmentID = info['departmentID']
        areaName = info['areaName']

        try:
            (status, reason) = self.__dupCheck(info=info)
            if status is not True:
                return (False, ErrorInfo['TENDER_47'])
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

    def __dupCheck(self, info):
        areaName = info['areaName'].strip()
        result = db.session.query(DepartmentArea).filter(
            DepartmentArea.areaName == areaName
        ).first()
        if result is not None:
            return (False, None)
        else:
            return (True, None)

    # 更改部门名称
    def updateDepartmentAreaName(self, info):
        areaID = info['areaID']
        areaName = info['areaName']
        try:
            (status, reason) = self.__dupCheck(info=info)
            if status is not True:
                return (False, ErrorInfo['TENDER_47'])
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

    def getAreaByID(self, info):
        areaID = info['areaID']

        try:
            query = db.session.query(DepartmentArea).filter(
                DepartmentArea.areaID == areaID
            )
            result = query.first()
            dataResult = {}
            dataResult.update(DepartmentArea.generate(o=result))
            return (True, dataResult)
        except Exception as e:
            print e
            traceback.print_exc()
            errorInfo = ErrorInfo['TENDER_02']
            errorInfo['detail'] = str(e)
            db.session.rollback()
            return (False, errorInfo)

    def getAreaTreeWithoutUserID(self, jsonInfo):
        info = json.loads(jsonInfo)
        tokenID = info['tokenID']
        (status, userID) = self.isTokenValid(tokenID)
        if status is not True:
            errorInfo = ErrorInfo['TENDER_01']
            return (False, errorInfo)
        info['userID'] = userID
        userBaseManager = UserBaseManager()
        (status, userInfo) = userBaseManager.getUserInfo(info=info)
        if status is not True:
            return (False, userInfo)
        userType = userInfo['userType']
        departmentRightManager = DepartmentRightManager()
        (status, rightDic) = departmentRightManager.getRightDicByUserID(info=info)
        if status is not True:
            return (False, rightDic)
        try:
            query = db.session.query(Department, DepartmentArea, DepartmentRight).outerjoin(
                DepartmentArea, Department.departmentID == DepartmentArea.departmentID
            )

            allResult = query.all()
            departmentDic = {}
            areaDic = {}
            def __generate(o, departmentDic):
                department = o.Department
                area = o.DepartmentArea

                departmentID = department.departmentID
                # if userType != USER_TAG_BOSS and not rightDic.has_key(departmentID):
                #     return None
                # 先将所有的department加入，然后再遍历一遍，将areaList为空的去掉
                if not departmentDic.has_key(departmentID):
                    res = {}
                    areaList = []
                    if area is not None:
                        areaID = area.areaID
                        if userType == USER_TAG_BOSS or rightDic.has_key(areaID):
                            if not areaDic.has_key(areaID):
                                areaObject = DepartmentArea.generate(o=area)
                                areaList.append(areaObject)
                                areaDic[areaID] = True
                    departmentDic[departmentID] = areaList
                    res['departmentID'] = departmentID
                    res['departmentName'] = department.departmentName
                    res['areaList'] = areaList
                    return res
                else:
                    if area is not None:
                        areaID = area.areaID
                        if userType == USER_TAG_BOSS or rightDic.has_key(area.areaID):
                            if not areaDic.has_key(areaID):
                                areaList = departmentDic[departmentID]
                                areaObject = DepartmentArea.generate(o=area)
                                areaList.append(areaObject)
                                areaDic[areaID] = True

            departmentList = [__generate(o=o, departmentDic=departmentDic) for o in allResult]
            departmentList = filter(None, departmentList)
            if userType != USER_TAG_BOSS:
                departmentList = [o for o in departmentList if len(o['areaList'])>0 or rightDic.has_key(o['departmentID'])]
            return (True, departmentList)

        except Exception as e:
            print e
            traceback.print_exc()
            errorInfo = ErrorInfo['TENDER_02']
            errorInfo['detail'] = str(e)
            db.session.rollback()
            return (False, errorInfo)


    def getAreaTree(self, info):
        departmentRightManager = DepartmentRightManager()
        (status, rightDic) = departmentRightManager.getRightDicByUserID(info=info)
        if status is not True:
            return (False, rightDic)
        try:
            query = db.session.query(Department, DepartmentArea).outerjoin(
                DepartmentArea, Department.departmentID == DepartmentArea.departmentID
            )

            allResult = query.all()
            departmentDic = {}
            def __generate(o, departmentDic):
                department = o.Department
                area = o.DepartmentArea

                departmentID = department.departmentID
                if not departmentDic.has_key(departmentID):
                    res = {}
                    areaList = []
                    if area is not None:
                        areaObject = DepartmentArea.generate(o=area)
                        if rightDic.has_key(areaObject['areaID']):
                            areaObject['hasRight'] = True
                            areaObject['rightID'] = rightDic[areaObject['areaID']]
                        else:
                            areaObject['hasRight'] = False
                        areaList.append(areaObject)
                    departmentDic[departmentID] = areaList
                    res['departmentID'] = departmentID
                    res['departmentName'] = department.departmentName
                    res['areaList'] = areaList
                    if rightDic.has_key(departmentID):
                        res['hasRight'] = True
                        res['rightID'] = rightDic[departmentID]
                    else:
                        res['hasRight'] = False
                    return res
                else:
                    areaList = departmentDic[departmentID]
                    areaObject = DepartmentArea.generate(o=area)
                    if rightDic.has_key(areaObject['areaID']):
                        areaObject['hasRight'] = True
                        areaObject['rightID'] = rightDic[areaObject['areaID']]
                    else:
                        areaObject['hasRight'] = False
                    areaList.append(areaObject)

            departmentList = [__generate(o=o, departmentDic=departmentDic) for o in allResult]
            departmentList = filter(None, departmentList)
            return (True, departmentList)

        except Exception as e:
            print e
            traceback.print_exc()
            errorInfo = ErrorInfo['TENDER_02']
            errorInfo['detail'] = str(e)
            db.session.rollback()
            return (False, errorInfo)