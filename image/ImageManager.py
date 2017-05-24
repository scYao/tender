# coding=utf8
import sys

reload(sys)
sys.setdefaultencoding('utf-8')
sys.path.append('..')

import json
from models.flask_app import db
import jieba

from models.ImgPath import ImgPath
from tool.config import ErrorInfo
from tool.Util import Util
from sqlalchemy import and_, func
from datetime import datetime
from pypinyin import lazy_pinyin

class ImageManager(Util):

    def __init__(self):
        self.ossInfo = {}
        self.ossInfo['bucket'] = 'sjtender'

    # 增加图片操作
    def addImage(self, info):
        imgList = info['imgList']
        foreignID = info['foreignID']
        if info.has_key('tag'):
            tag = info['tag']
        else:
            tag = 0

        index = 0
        for img in imgList:
            imgName = img['imgName']
            imgNum = img['imgNum']
            imgID = self.generateID(str(index) + imgName)
            imagePath = ImgPath(imgPathID=imgID, path=imgName, foreignID=foreignID,
                                tag=tag, imgNum=imgNum)
            db.session.add(imagePath)
            index = index + 1

        return (True, None)

    def doesImageExists(self, jsonInfo):
        info = json.loads(jsonInfo)
        foreignID = info['foreignID']
        imgNum = info['imgNum']

        try:
            result = db.session.query(ImgPath).filter(
                # and_(ImgPath.foreignID == foreignID,
                #      ImgPath.imgNum == imgNum)
                ImgPath.imgNum == imgNum
            ).first()
            if result is not None:
                return (True, result.imgPathID)
            else:
                return (False, None)
        except Exception as e:
            print str(e)
            # traceback.print_stack()
            db.session.rollback()
            errorInfo = ErrorInfo['TENDER_02']
            errorInfo['detail'] = str(e)
            return (False, errorInfo)


    def addImagesWithOSS(self, info):
        imgList = info['imgList']
        directory = info['directory']
        foreignID = info['foreignID']

        ossInfo = {}
        ossInfo['bucket'] = 'sjtender'
        index = 0

        for img in imgList:
            imgID = self.generateID(str(index) + img['imgPath'])
            path = imgID + img['imgPath']
            imgFile = img['imgFile']
            imagePath = ImgPath(imgPathID=imgID, path=path, foreignID=foreignID)
            db.session.add(imagePath)
            index = index + 1
            self.uploadOSSImage('%s/%s' % (directory, path), ossInfo, imgFile)

        return (True, None)


    def deleteImage(self, info):
        imgPathID = info["imgPathID"]
        directory = info['directory']

        deleteList = []

        ossInfo = {}
        ossInfo['bucket'] = 'sjtender'
        try:
            deleteQuery = db.session.query(ImgPath).filter(
                ImgPath.imgPathID == imgPathID
            )
            imgPath = deleteQuery.first()
            deleteList.append('%s/%s' % (directory, imgPath.path))
            deleteQuery.delete(synchronize_session=False)
            self.deleteOSSImages(deleteList, ossInfo)
            db.session.commit()
        except Exception as e:
            print e
            errorInfo = ErrorInfo['TENDER_51']
            errorInfo['detail'] = str(e)
            return (False, errorInfo)

        return (True, None)

    # 删除图片操作
    def deleteImgList(self, info):
        deleteImgIDList = info["deleteImgIDList"]
        if info.has_key('directory'):
            directory = info['directory']
        else:
            directory = 'merchandise'
        deleteList = []
        for img in deleteImgIDList:
            deleteQuery = db.session.query(ImgPath).filter(
                ImgPath.imgPathID == img
            )
            imgPath = deleteQuery.first()
            deleteList.append('%s/%s' % (directory, imgPath.path))
            deleteQuery.delete(synchronize_session=False)

        ossInfo = {}
        ossInfo['bucket'] = 'sjsecondhand'
        try:
            if len(deleteList) > 0:
                self.deleteOSSImages(deleteList, ossInfo)
        except Exception as e:
            print e
            errorInfo = ErrorInfo['SPORTS_44']
            errorInfo['detail'] = str(e)
            return (False, errorInfo)

        return (True, None)

    def deleteImagesByForeignID(self, info):
        foreignID = info['foreignID']
        directory = info['directory']

        query = db.session.query(ImgPath).filter(
            ImgPath.foreignID == foreignID
        )

        allResult = query.all()

        deleteList = ['%s/%s' % (directory, i.path) for i in allResult]
        ossInfo = {}
        ossInfo['bucket'] = 'sjsecondhand'
        try:
            query.delete(synchronize_session=False)
            if len(deleteList) > 0:
                self.deleteOSSImages(deleteList, ossInfo)
        except Exception as e:
            print e
            errorInfo = ErrorInfo['SPORTS_44']
            errorInfo['detail'] = str(e)
            return (False, errorInfo)

        return (True, None)



    # 从oss删除图片, 图片不在imgPath表里存储
    def deleteImgFromOSS(self, info):
        imgPath = info['imgPath']
        if info.has_key('directory'):
            directory = info['directory']
        else:
            directory = 'merchandise'

        ossInfo = {}
        ossInfo['bucket'] = 'sjsecondhand'
        try:
            deleteList = ['%s/%s' % (directory, imgPath)]
            self.deleteOSSImages(deleteList, ossInfo)
        except Exception as e:
            print e
            errorInfo = ErrorInfo['SPORTS_44']
            errorInfo['detail'] = str(e)
            return (False, errorInfo)

        return (True, None)

    # 上传图片到oss
    def uploadImageToOSS(self, info):
        imgPath = info['imgPath']
        if info.has_key('directory'):
            directory = info['directory']
        else:
            directory = 'merchandise'

        imgFile = info['imgFile']

        ossInfo = {}
        ossInfo['bucket'] = 'sjsecondhand'
        try:
            self.uploadOSSImage('%s/%s' % (directory, imgPath), ossInfo, imgFile)
        except Exception as e:
            print e
            errorInfo = ErrorInfo['SPORTS_43']
            errorInfo['detail'] = str(e)
            return (False, errorInfo)
        return (True, None)

    #获取物流公司图片
    def getLogisticsCompanyImg(self, imgPath):
        ossInfo = {}
        ossInfo['bucket'] = 'sjsecondhand'
        res = {}
        ossInfo['objectKey'] = 'logisticsCompany/%s@!constrain-300h' % imgPath
        res['path'] = self.getSecurityUrl(ossInfo)
        return (True, res)

    #获取演唱会图片列表
    def getCountableMerchandiseTypeImgList(self, foreignID):
        allResult = db.session.query(ImgPath).filter(
            ImgPath.foreignID == foreignID
        ).all()
        ossInfo = {}
        ossInfo['bucket'] = 'sjsecondhand'
        def generateImg(img):
            ossInfo['objectKey'] = 'countableMerchandiseType/%s@!constrain-300h' % img.path
            path = self.getSecurityUrl(ossInfo)
            return path
        imgList = [generateImg(img) for img in allResult]
        return (True, imgList)



    # 获取实名认证中图片列表
    def getCertificationImgList(self, info):
        foreignID = info['foreignID']
        allResult = db.session.query(ImgPath).filter(
            ImgPath.foreignID == foreignID
        ).all()
        ossInfo = {}
        ossInfo['bucket'] = 'sjsecondhand'
        def generateImg(img):
            res = {}
            res['imgPathID'] = img.imgPathID
            ossInfo['objectKey'] = 'certification/%s@!constrain-300h' % img.path
            res['path'] = self.getSecurityUrl(ossInfo)
            return res

        imgList = [generateImg(img) for img in allResult]
        return (True, imgList)

    # 更新图片, 二手街, 专题等
    def updateItemImageBackground(self, info, imgFile):
        itemID = info['itemID']
        directory = info['directory']

        allResult = db.session.query(ImgPath).filter(
            ImgPath.foreignID == itemID
        ).all()

        # 1, 先删除二手街的图片, 及在oss上的文件
        imgIDList = [i.imgPathID for i in allResult]
        imgManager = ImageManager()
        deleteImgInfo = {}
        deleteImgInfo['deleteImgIDList'] = imgIDList
        deleteImgInfo['directory'] = directory
        imgManager.deleteImgList(deleteImgInfo)

        # 2, 上传新图片
        imgPath = info['imgPath']
        imgName = self.generateID(imgPath) + imgPath
        deleteImgInfo['foreignID'] = itemID
        deleteImgInfo['imgList'] = [imgName]

        ossInfo = {}
        ossInfo['bucket'] = 'sjsecondhand'
        try:
            imgManager.addImage(deleteImgInfo)
            self.uploadOSSImage('%s/%s' % (directory, imgName), ossInfo, imgFile)
        except Exception as e:
            print e
            errorInfo = ErrorInfo['SPORTS_16']
            errorInfo['detail'] = str(e)
            return (False, errorInfo)
        return (True, None)


    def addImageListWithoutOSS(self, info):
        imgList = info['imgList']
        foreignID = info['foreignID']
        try:
            for img in imgList:
                imgPath = img['imgPath']
                imgName = img['imgName']
                imageID = self.generateID(imgPath)
                _img = ImgPath(imgPathID=imageID, path=imgPath,
                               foreignID=foreignID, imgName=imgName)
                db.session.add(_img)

            db.session.commit()
        except Exception as e:
            print e
            errorInfo = ErrorInfo['TENDER_02']
            errorInfo['detail'] = str(e)
            return (False, errorInfo)
        return (True, None)

    def getImageList(self, info):
        foreignID = info['foreignID']
        startIndex = info['startIndex']
        pageCount = info['pageCount']
        try:
            query = db.session.query(ImgPath).filter(
                ImgPath.foreignID == foreignID
            ).offset(startIndex).limit(pageCount)
            countQuery = db.session.query(func.count()).filter(
                ImgPath.foreignID == foreignID
            )
            allResult = query.all()
            def __generateImg(o):
                res = {}
                res.update(ImgPath.generate(img=o, ossInfo=self.ossInfo, directory='contract', isFile=True))
                return res
            dataList = [__generateImg(o=o) for o in allResult]
            count = countQuery.first()
            if count is None:
                count = 0
            else:
                count = count[0]
            dataInfo = {}
            dataInfo['dataList'] = dataList
            dataInfo['count'] = count
            return (True, dataInfo)
        except Exception as e:
            print e
            errorInfo = ErrorInfo['TENDER_02']
            errorInfo['detail'] = str(e)
            return (False, errorInfo)
