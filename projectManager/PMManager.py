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
from datetime import datetime
from pypinyin import lazy_pinyin
from sqlalchemy import desc
from models.flask_app import db
from models.ProjectManager import ProjectManager
from models.SearchKey import SearchKey

from tool.Util import Util
from tool.config import ErrorInfo
from image.ImageManager import ImageManager


class PMManager(Util):

    def __init__(self):
        pass

    # 创建公司
    def createProjectManager(self, jsonInfo):
        info = json.loads(jsonInfo)
        managerName = info['managerName'].replace('\'', '\\\'').replace('\"', '\\\"')
        gender = info['gender'].replace('\'', '\\\'').replace('\"', '\\\"')
        positionalTitles = info['positionalTitles'].replace('\'', '\\\'').replace('\"', '\\\"')
        post = info['post'].replace('\'', '\\\'').replace('\"', '\\\"')
        safetyAssessment = info['safetyAssessment'].replace('\'', '\\\'').replace('\"', '\\\"')
        safeEndDate = info['safeEndDate'].replace('\'', '\\\'').replace('\"', '\\\"')
        safeAuthority = info['safeAuthority'].replace('\'', '\\\'').replace('\"', '\\\"')
        safeFromDate = info['safeFromDate'].replace('\'', '\\\'').replace('\"', '\\\"')
        companyID = info['companyID'].replace('\'', '\\\'').replace('\"', '\\\"')

        managerID = self.generateID(managerName)

        projectManager = ProjectManager(
            managerID=managerID, managerName=managerName, gender=gender,
            positionalTitles=positionalTitles, post=post,
            safetyAssessment=safetyAssessment, safeEndDate=safeEndDate, safeAuthority=safeAuthority,
            safeFromDate=safeFromDate, companyID=companyID
        )
        try:
            db.session.add(projectManager)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print e
            errorInfo = ErrorInfo['TENDER_02']
            errorInfo['detail'] = str(e)
            return (False, errorInfo)
        return (True, managerID)

    def getProjectManagerList(self, jsonInfo):
        info = json.loads(jsonInfo)
        companyID = info['companyID']
        startIndex = info['startIndex']
        pageCount = info['pageCount']

        query = db.session.query(ProjectManager)
        if info.has_key('searchKey'):
            searchKey = info['searchKey']
            if len(searchKey) == 1:
                searchKey = " ".join(lazy_pinyin(searchKey))
            if searchKey != '':
                query = SearchKey.query.whoosh_search(searchKey).outerjoin(
                    ProjectManager, ProjectManager.managerID == SearchKey.tenderID
                )