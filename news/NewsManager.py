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
from datetime import datetime
from sqlalchemy import desc, and_
from models.flask_app import db
from models.News import News
from models.ImgPath import ImgPath

from tool.tagconfig import TENDER_NEWS
from tool.Util import Util
from tool.config import ErrorInfo
from sqlalchemy import func


class NewsManager(Util):

    def __init__(self):
        pass

    def createNews(self, jsonInfo, imgFileList):
        info = json.loads(jsonInfo)
        title = info['title'].replace('\'', '\\\'').replace('\"', '\\\"').strip()
        content = info['content'].replace('\'', '\\\'').replace('\"', '\\\"')

        newsID = self.generateID(title)
        ossInfo = {}
        ossInfo['bucket'] = 'sjtender'
        try:
            index = 0
            for i in imgFileList:
                imgID = self.generateID(str(index) + i['imgName'])
                postFix = str(i['imgName']).split('.')
                if len(postFix) > 0:
                    postFix = '.' + postFix[-1]
                else:
                    postFix = ''
                imgPath = imgID + postFix
                imagePath = ImgPath(imgPathID=imgID, path=imgPath,
                                    foreignID=newsID, imgName=i['imgName'])
                db.session.add(imagePath)
                index = index + 1
                self.uploadOSSImage('tendernews/%s' % imgPath, ossInfo, i['file'])

            # 增加资讯记录
            now = datetime.now()
            news = News(newsID=newsID, title=title, content=content, createTime=now)
            db.session.add(news)
            db.session.commit()
            return (True, newsID)
        except Exception as e:
            print e
            traceback.print_exc()
            print 'upload file to oss error'
            errorInfo = ErrorInfo['TENDER_31']
            errorInfo['detail'] = str(e)
            return (False, errorInfo)

    # 获取资讯列表
    def getNewsList(self, jsonInfo):
        info = json.loads(jsonInfo)
        startIndex = info['startIndex']
        pageCount = info['pageCount']
        # 获取tenderID列表
        try:
            query = db.session.query(News)
            # count
            countQuery = db.session.query(func.count(News.newsID))
            count = countQuery.first()
            count = count[0]
            resultResult = query.order_by(
                desc(News.createTime)
            ).offset(startIndex).limit(pageCount).all()
            dataList = [News.generateBrief(o=o) for o in resultResult]
            newsIDList = [o.newsID for o in resultResult]
            info['newsIDList'] = newsIDList
            info['dataList'] = dataList
            self.addImageListToNews(info=info)
            callBackInfo = {}
            callBackInfo['dataList'] = dataList
            callBackInfo['count'] = count
            return (True, callBackInfo)
        except Exception as e:
            print e
            traceback.print_exc()
            errorInfo = ErrorInfo['TENDER_02']
            errorInfo['detail'] = str(e)
            db.session.rollback()
            return (False, errorInfo)

    def __generateImg(self, o, dic, ossInfo):
        foreignID = o.foreignID
        img = ImgPath.generate(img=o, directory=TENDER_NEWS, ossInfo=ossInfo,
                                                hd=True, isFile=False)

        if not dic.has_key(foreignID):
            imgList = [img]
            dic[foreignID] = imgList
            print dic
        else:
            imgList = dic[foreignID]
            imgList.append(img)
        return (True, None)

    def addImageListToNews(self, info):
        newsIDList = info['newsIDList']
        dataList = info['dataList']

        allResult = db.session.query(ImgPath).filter(
            ImgPath.foreignID.in_(tuple(newsIDList))
        ).all()

        dic = {}
        ossInfo = {}
        ossInfo['bucket'] = 'sjtender'
        _ = [self.__generateImg(o=o, dic=dic, ossInfo=ossInfo) for o in allResult]
        for o in dataList:
            newsID = o['newsID']
            o['imgList'] = dic[newsID]
        def __addImgList(o):
            o['imgList'] = dic[o['newsID']]
        _ = [__addImgList(o=o) for o in dataList]
        return (True, None)


    def getNewsDetail(self, jsonInfo):
        info = json.loads(jsonInfo)
        newsID = info['newsID']

        try:
            result = db.session.query(News).filter(
                News.newsID == newsID
            ).first()

            newsResult = {}
            newsResult.update(News.generate(o=result))
            imgResult = db.session.query(ImgPath).filter(
                ImgPath.foreignID == newsResult['newsID']
            ).all()
            ossInfo = {}
            ossInfo['bucket'] = 'sjtender'
            newsResult['imgList'] = [ImgPath.generate(img=o, directory=TENDER_NEWS, ossInfo=ossInfo,
                                                hd=True, isFile=False) for o in imgResult]
            return (True, newsResult)
        except Exception as e:
            print e
            traceback.print_exc()
            errorInfo = ErrorInfo['TENDER_02']
            errorInfo['detail'] = str(e)
            db.session.rollback()
            return (False, errorInfo)

    def deleteNewsBackground(self, jsonInfo):
        info = json.loads(jsonInfo)
        newsID = info['newsID']

        try:
            db.session.query(News).filter(
                News.newsID == newsID
            ).delete(synchronize_session=False)
        except Exception as e:
            print e
            traceback.print_exc()
            errorInfo = ErrorInfo['TENDER_02']
            errorInfo['detail'] = str(e)
            db.session.rollback()
            return (False, errorInfo)
