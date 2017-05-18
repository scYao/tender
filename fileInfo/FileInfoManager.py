# coding=utf8
import sys


reload(sys)
sys.setdefaultencoding('utf-8')
sys.path.append('..')
from  datetime import datetime
import xmltodict
import traceback
from sqlalchemy import func, desc, and_, or_
import json
from tool.Util import Util
from tool.config import ErrorInfo
from tool.tagconfig import USER_TAG_BOSS
from models.flask_app import db
from models.FileInfo import FileInfo
from models.DepartmentArea import DepartmentArea

from user.UserBaseManager import UserBaseManager
from department.DepartmentRightManager import DepartmentRightManager

class FileInfoManager(Util):

    def __init__(self):
        self.ossInfo = {}
        self.ossInfo['bucket'] = 'sjtender'

    def doCreateFileInfo(self, info, userID):
        fileName = info['fileName']
        superID = info['superID']
        isDirectory = info['isDirectory']
        privateLevel = info['privateLevel']
        filePath = info['filePath']
        areaID = info['areaID']

        fileID = self.generateID(fileName)
        now = datetime.now()
        fileInfo = FileInfo(fileID=fileID, fileName=fileName,
                            userID=userID, createTime=now,
                            superID=superID, isDirectory=isDirectory,
                            privateLevel=privateLevel, filePath=filePath,
                            areaID=areaID)
        db.session.add(fileInfo)
        return (True, None)

    def createFileInfo(self, jsonInfo):
        info = json.loads(jsonInfo)
        tokenID = info['tokenID']
        (status, userID) = self.isTokenValid(tokenID)
        if status is not True:
            errorInfo = ErrorInfo['TENDER_01']
            return (False, errorInfo)
        fileList = info['fileList']

        try:
            _ = [self.doCreateFileInfo(info=f, userID=userID) for f in fileList]
            db.session.commit()
            return (True, None)
        except Exception as e:
            print e
            traceback.print_exc()
            errorInfo = ErrorInfo['TENDER_02']
            errorInfo['detail'] = str(e)
            db.session.rollback()
            return (False, errorInfo)

    # 查看我的上传列表
    def getMyFileList(self, jsonInfo):
        info = json.loads(jsonInfo)
        tokenID = info['tokenID']
        (status, userID) = self.isTokenValid(tokenID)
        if status is not True:
            errorInfo = ErrorInfo['TENDER_01']
            return (False, errorInfo)
        startIndex = info['startIndex']
        pageCount = info['pageCount']
        try:
            query = db.session.query(FileInfo, DepartmentArea).outerjoin(
                DepartmentArea, FileInfo.areaID == DepartmentArea.areaID
            )
            countQuery = db.session.query(func.count(FileInfo.fileID)).filter(
                FileInfo.userID == userID
            )
            query = query.filter(
                FileInfo.userID == userID
            ).offset(startIndex).limit(pageCount)

            def __generateFileInfo(o):
                res = {}
                fileInfo = o.FileInfo
                area = o.DepartmentArea
                res.update(FileInfo.generate(o=fileInfo, ossInfo=self.ossInfo))
                res.update(DepartmentArea.generate(o=area))
                return res
            allResult = query.all()
            count = countQuery.first()
            if count is not None:
                count = count[0]
            else:
                count = 0
            dataList = [__generateFileInfo(o=o) for o in allResult]
            dataResult = {}
            dataResult['count'] = count
            dataResult['dataList'] = dataList
            return (True, dataResult)
        except Exception as e:
            print e
            traceback.print_exc()
            errorInfo = ErrorInfo['TENDER_02']
            errorInfo['detail'] = str(e)
            db.session.rollback()
            return (False, errorInfo)

    # 查看所有的文件 共管理员用户使用
    def getAllFileList(self, info):
        pass

    def __getBaseQuery(self, info):
        query = db.session.query(FileInfo)
        countQuery = db.session.query(func.count(FileInfo.fileID))
        info['query'] = query
        info['countQuery'] = countQuery
        return info

    def __addFilterToQuery(self, info):
        superID = info['superID']
        query = info['query']
        countQuery = info['countQuery']
        startIndex = info['startIndex']
        pageCount = info['pageCount']
        areaID = info['areaID']
        userType = info['userType']

        departmentRightManager = DepartmentRightManager()
        (status, areaIDList) = departmentRightManager.getAreaListByUserID(info=info)

        query = query.filter(and_(FileInfo.superID == superID,
                                  FileInfo.areaID == areaID))

        countQuery = countQuery.filter(and_(FileInfo.superID == superID,
                                            FileInfo.areaID == areaID))


        if userType != USER_TAG_BOSS:
            query = query.filter(FileInfo.areaID.in_(tuple(areaIDList)))
            countQuery = countQuery.filter(FileInfo.areaID.in_(tuple(areaIDList)))


        query = query.order_by(desc(
            FileInfo.createTime
        )).offset(startIndex).limit(pageCount)
        info['query'] = query
        info['countQuery'] = countQuery
        return info

    def __generateFileInfo(self, o):
        res = {}
        res.update(FileInfo.generate(o=o, ossInfo=self.ossInfo))
        return res


    def getFileListByUser(self, jsonInfo):
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

        info['userType'] = userType
        info = self.__getBaseQuery(info=info)
        info = self.__addFilterToQuery(info=info)
        query = info['query']
        countQuery = info['countQuery']
        dataResult = {}

        allResult = query.all()
        dataList = [self.__generateFileInfo(o=o) for o in allResult]
        count = countQuery.first()
        if count is None:
            count = 0
        else:
            count = count[0]
        dataResult['dataList'] = dataList
        dataResult['count'] = count
        return (True, dataResult)


    # 删除某个文件
    def deleteFileInfo(self, info):
        userID = info['userID']
        fileID = info['fileID']

        try:
            # 先删除oss文件

            query = db.session.query(FileInfo).filter(
                FileInfo.fileID == fileID
            )

            dataResult = query.first()

            if dataResult is None:
                return (False, ErrorInfo['TENDER_40'])
            # 文件夹暂时不让删除
            if dataResult.isDirectory is True:
                superID = dataResult.fileID
                # 查看文件夹下是否有文件
                dirResult = db.session.query(FileInfo).filter(
                    FileInfo.superID == superID
                ).first()
                if dirResult is not None:
                    return (FileInfo, ErrorInfo['TENDER_45'])
                query.delete(synchronize_session=False)
                db.session.commit()
                return (True, None)
                # return (False, ErrorInfo['TENDER_40'])
            filePath = dataResult.filePath
            deleteList = ['files/%s' % filePath]
            self.deleteOSSImages(deleteList, self.ossInfo)

            createUserID = dataResult.userID
            # 先判断是否是文件的创建者
            if userID != createUserID:
                userBaseManager = UserBaseManager()
                (status, userInfo) = userBaseManager.getUserInfo(info=info)
                if status is not True:
                    return (False, userInfo)
                userType = userInfo['userType']
                # 只有boss才能删除
                if userType != USER_TAG_BOSS:
                    return (False, ErrorInfo['TENDER_39'])
            query.delete(synchronize_session=False)
            db.session.commit()
            return (True, None)
        except Exception as e:
            print e
            traceback.print_exc()
            errorInfo = ErrorInfo['TENDER_02']
            errorInfo['detail'] = str(e)
            db.session.rollback()
            return (False, errorInfo)

    # 删除我的文件
    def deleteFileByUser(self, jsonInfo):
        info = json.loads(jsonInfo)
        tokenID = info['tokenID']
        (status, userID) = self.isTokenValid(tokenID)
        if status is not True:
            errorInfo = ErrorInfo['TENDER_01']
            return (False, errorInfo)

        info['userID'] = userID
        return self.deleteFileInfo(info=info)

    # 管理员删除文件
    def deleteFileByManager(self, jsonInfo):
        pass


    def renameDirectory(self, info):
        fileID = info['fileID']
        userID = info['userID']
        fileName = info['fileName'].strip()

        try:
            query = db.session.query(FileInfo).filter(
                FileInfo.fileID == fileID
            )

            result = query.first()

            if result is None:
                return (False, ErrorInfo['TENDER_48'])

            fileUserID = result.userID
            if userID != fileUserID:
                return (False, ErrorInfo['TENDER_49'])

            query.update(
                {
                    FileInfo.fileName : fileName
                },
                synchronize_session=False
            )
            db.session.commit()
            return (True, fileID)
        except Exception as e:
            print e
            traceback.print_exc()
            errorInfo = ErrorInfo['TENDER_02']
            errorInfo['detail'] = str(e)
            db.session.rollback()
            return (False, errorInfo)