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

from user.UserBaseManager import UserBaseManager


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

        fileID = self.generateID(fileName)
        now = datetime.now()
        fileInfo = FileInfo(fileID=fileID, fileName=fileName,
                            userID=userID, createTime=now,
                            superID=superID, isDirectory=isDirectory,
                            privateLevel=privateLevel, filePath=filePath)
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

        query = query.filter(FileInfo.superID == superID)
        countQuery = countQuery.filter(FileInfo.superID == superID)

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
                return (False, ErrorInfo['TENDER_40'])
            filePath = dataResult.filePath
            deleteList = ['files/%s' % filePath]
            self.deleteOSSImages(deleteList, self.ossInfo)

            createUserID = dataResult.userID
            # 先判断是否是文件的创建者
            if userID != createUserID:
                userBaseManager = UserBaseManager()
                userInfo = userBaseManager.getUserInfo(info=info)
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