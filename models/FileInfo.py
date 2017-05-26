# -*- coding: utf-8 -*-
import os
import sys

reload(sys)
sys.setdefaultencoding('utf-8')
from flask_app import db

from tool.Util import Util

class FileInfo(db.Model):
    __tablename__ = 'FileInfo'
    fileID = db.Column(db.String(100), primary_key=True)
    fileName = db.Column(db.String(100))
    userID = db.Column(db.String(100))
    createTime = db.Column(db.DateTime)
    superID = db.Column(db.String(100))
    isDirectory = db.Column(db.Boolean)
    privateLevel = db.Column(db.Integer)
    filePath = db.Column(db.String(1000))
    areaID = db.Column(db.String(100))
    tag = db.Column(db.Integer)


    def __init__(self, fileID=None, fileName=None,
                 userID=None, createTime=None, superID='-1',
                 isDirectory=False, privateLevel=0, filePath=None,
                 areaID=None, tag=0):
        self.fileID = fileID
        self.fileName = fileName
        self.userID = userID
        self.createTime = createTime
        self.superID = superID
        self.isDirectory = isDirectory
        self.privateLevel = privateLevel
        self.filePath = filePath
        self.areaID = areaID
        self.tag = tag

    @staticmethod
    def generate(o, ossInfo):
        res = {}
        res['fileID'] = o.fileID
        res['fileName'] = o.fileName
        res['userID'] = o.userID
        res['isDirectory'] = o.isDirectory
        res['tag'] = o.tag
        res['createTime'] = str(o.createTime)

        util = Util()
        if o.isDirectory is False:
            ossInfo['objectKey'] = '%s/%s' % ('files', o.filePath)
            res['filePath'] = util.getSecurityFileUrl(ossInfo)
        return res


    def __repr__(self):
        return self.fileID