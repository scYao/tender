# coding=utf8
import sys
import traceback
import urllib2
import poster
import requests

sys.path.append("..")
import os
reload(sys)
sys.setdefaultencoding('utf-8')
import json
from models.flask_app import db, cache
from datetime import datetime, timedelta
from pypinyin import lazy_pinyin
from tool.Util import Util
from tool.config import ErrorInfo
from models.SearchKey import SearchKey
from models.PushedTenderInfo import PushedTenderInfo
from models.ImgPath import ImgPath
from models.Tender import Tender
from models.CustomizedTender import CustomizedTender
from tool.tagconfig import SEARCH_KEY_TAG_TENDRE, PUSH_TENDER_INFO_TAG_CUS
from sqlalchemy import desc, and_, func

class CustomizedTenderManager(Util):
    def __init__(self):
        pass

    def __doCreateCustomizedTender(self, info):
        title = info['title']
        userID = info['userID']
        tenderID = self.generateID(title + userID)
        info['tenderID'] = tenderID
        now = datetime.now()
        # return CustomizedTender.create(info=info)
        url = info['url']
        tenderTag = info['tenderTag']
        tender = Tender(tenderID=tenderID, title=title, userID=userID, url=url,
                        publishDate=now, typeID='-1', cityID='63', tenderTag=tenderTag)
        db.session.add(tender)
        return (True, tenderID)



    def createCustomizedTender(self, info, imgFileList):
        userID = info['userID']
        ossInfo = {}
        ossInfo['bucket'] = 'sjtender'
        try:
            info['userID'] = userID
            info['tenderTag'] = PUSH_TENDER_INFO_TAG_CUS
            (status, tenderID) = self.__doCreateCustomizedTender(info=info)
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
                                    foreignID=tenderID, imgName=i['imgName'])
                db.session.add(imagePath)
                index = index + 1
                self.uploadOSSImage('customizedtender/%s' % imgPath, ossInfo, i['file'])
            db.session.commit()
            return (True, tenderID)
        except Exception as e:
            print e
            traceback.print_exc()
            print 'upload file to oss error'
            errorInfo = ErrorInfo['TENDER_31']
            errorInfo['detail'] = str(e)
            return (False, errorInfo)
