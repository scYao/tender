# coding=utf8
import base64
import hmac
import random
import re
import sys
import urllib

from tool.config import ErrorInfo

sys.path.append('..')
import hashlib
import time
import json
import oss2
import datetime
from models.flask_app import db
from models.Token import Token

class Util:
    def __init__(self):
        pass

    def uploadOSSImage(self, imageName, ossInfo, imgFile):
        bucket = self._getBucket(ossInfo)
        return bucket.put_object(imageName, imgFile)

    def deleteOSSImages(self, imageList, ossInfo):
        bucket = self._getBucket(ossInfo)
        return bucket.batch_delete_objects(imageList)

    def getRandomStr(self):
        return str(random.uniform(1, 10000))

    def getSecurityUrl(self, ossInfo):
        obj = ossInfo['objectKey']
        bucket = self._getBucket(ossInfo, endpoint='img-cn-hangzhou.aliyuncs.com')
        return bucket.sign_url('GET', obj, 3600)

    def _getBucket(self, ossInfo, endpoint='oss-cn-hangzhou.aliyuncs.com'):
        bucketStr = ossInfo['bucket']
        OSSAccessKeyId = 'HReEC1sQufBRLcQC'
        secret = '5rqWY7jXhGeF0HBhYpl10mSkgrrHZt'
        auth = oss2.Auth(OSSAccessKeyId, secret)
        _endpoint = endpoint
        return oss2.Bucket(auth, _endpoint, bucketStr)

    def getOssSignature(self, ossInfo):
        bucket = ossInfo['bucket']
        obj = ossInfo['objectKey']

        secret = '5rqWY7jXhGeF0HBhYpl10mSkgrrHZt'
        timeStamp = ossInfo['timeStamp']
        h = hmac.new(secret, 'GET\n\n\n%d\n/%s/%s' % (timeStamp, bucket, obj), hashlib.sha1)
        return urllib.quote_plus(base64.encodestring(h.digest()).strip())

    def getOSSUrl(self, ossInfo):
        bucket = ossInfo['bucket']
        obj = ossInfo['objectKey']
        timeStamp = self.datetime2Timestamp(self.getCurrentTime()) + 600
        ossInfo['timeStamp'] = timeStamp
        OSSAccessKeyId = 'HReEC1sQufBRLcQC'
        signature = self.getOssSignature(ossInfo)
        url = 'http://%s.img-cn-hangzhou.aliyuncs.com/%s?' \
              'Expires=%d&OSSAccessKeyId=%s&Signature=%s' % (bucket, obj, timeStamp, OSSAccessKeyId, signature)
        return url

    def datetime2Timestamp(self, dt):
        time.strptime(dt, '%Y-%m-%d %H:%M:%S')
        ## time.struct_time(tm_year=2012, tm_mon=3, tm_mday=28, tm_hour=6, tm_min=53, tm_sec=40, tm_wday=2, tm_yday=88, tm_isdst=-1)
        #将"2012-03-28 06:53:40"转化为时间戳
        s = time.mktime(time.strptime(dt, '%Y-%m-%d %H:%M:%S'))
        return int(s)

    def getMD5String(self, str):
        m = hashlib.md5()
        m.update(str)
        return m.hexdigest()

    def getCurrentTime(self):
        ISOTIMEFORMAT = '%Y-%m-%d %X'
        currentTime = time.strftime(ISOTIMEFORMAT, time.localtime())
        return currentTime

    def datetimeToString(self, dateTime):
        ISOTIMEFORMAT = '%Y-%m-%d'
        currentTime = time.strftime(ISOTIMEFORMAT, dateTime)
        return str(currentTime)

    def isTokenValid(self, tokenID):
        #判断tokenID 是否存在
        result = db.session.query(Token).filter(Token.tokenID==tokenID).first()
        if result is None:
            errorInfo = ErrorInfo['TENDER_01']
            errorInfo['detail'] = result
            return (False, errorInfo)
        createTime = result.createTime

        now = datetime.datetime.now()
        #将token登录时间更新为最近的一次操作时间
        db.session.query(Token).filter(
            Token.tokenID == tokenID
        ).update(
            {Token.createTime : now},
            synchronize_session=False)
        validity = result.validity
        try:
            db.session.commit()
        except Exception as e:
            print e
            errorInfo = ErrorInfo['SPORTS_02']
            errorInfo['detail'] = str(e)
            db.session.rollback()
            return (False, errorInfo)
        days = (now - createTime).days
        if days > validity:
            errorInfo = ErrorInfo['SPORTS_01']
            errorInfo['detail'] = result
            return (False, errorInfo)

        return (True, result.userID)

    def generateID(self, value):
        # currentTime = datetime.datetime.now()
        currentTime = self.getCurrentTime()
        #resultID = self.getMD5String(value.join(str(currentTime)))
        now = datetime.datetime.now()
        resultID = self.getMD5String(''.join([str(currentTime), value, str(now)]))
        resultID = ''.join([str(currentTime), resultID]).replace(' ','')
        resultID = ''.join(re.split(':', resultID))
        return resultID

    def generateCode(self, value):
        code = (hex(int(value)).upper())[2:]
        return code


if __name__ == '__main__':
    u = Util()
    print u.generateID('a')
    # print u.isTokenValid('2016-04-22154653e39f5af713d36a703d02e5516c45a565')
