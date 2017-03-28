# -*- coding: utf-8 -*-
import os
import sys

reload(sys)
sys.setdefaultencoding('utf-8')
from flask_app import db
from tool.Util import Util

class ImgPath(db.Model):
    __tablename__ = 'ImgPath'

    imgPathID = db.Column(db.String(100), primary_key=True)
    path = db.Column(db.Text)
    foreignID = db.Column(db.String(100))
    tag = db.Column(db.Integer)
    imgNum = db.Column(db.String(100))
    imgName = db.Column(db.Text)

    def __init__(self, imgPathID=None, path=None, foreignID=None,
                 tag=0, imgNum=None, imgName=None):
        self.imgPathID = imgPathID
        self.path = path
        self.foreignID = foreignID
        self.tag = tag
        self.imgNum = imgNum
        self.imgName = imgName

    @staticmethod
    def generate(img, ossInfo, directory, hd=None):
        res = {}
        res['imgPathID'] = img.imgPathID
        if hd is not None:
            ossInfo['objectKey'] = '%s/%s' % (directory, img.path)
        else:
            ossInfo['objectKey'] = '%s/%s@!constrain-300h' % (directory, img.path)
        util = Util()
        res['imgPath'] = util.getSecurityUrl(ossInfo)
        res['tag'] = img.tag
        res['imgName'] = img.imgName
        return res





    def __repr__(self):
        return self.imgPathID