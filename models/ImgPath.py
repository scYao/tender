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

    def __init__(self, imgPathID=None, path=None, foreignID=None,
                 tag=0):
        self.imgPathID = imgPathID
        self.path = path
        self.foreignID = foreignID
        self.tag = tag

    @staticmethod
    def generate(img, ossInfo, directory):
        res = {}
        res['imgPathID'] = img.imgPathID
        ossInfo['objectKey'] = '%s/%s@!constrain-300h' % (directory, img.path)
        util = Util()
        print ossInfo
        res['imgPath'] = util.getSecurityUrl(ossInfo)
        res['tag'] = img.tag
        return res


    def __repr__(self):
        return self.imgPathID