# coding=utf8
import base64
import hmac
import random
import re
import sys
import urllib
import xml.etree.ElementTree as ET
from tool.config import ErrorInfo
from tool.tagconfig import PUBLICAPPID, PUBLICSECRET, INTERVALTIME

sys.path.append('..')
import hashlib
import time
import json
import oss2
import datetime
from models.flask_app import db
from sqlalchemy import and_
from models.Token import Token
from models.AccessToken import AccessToken

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

    def getSecurityFileUrl(self, ossInfo):
        obj = ossInfo['objectKey']
        bucket = self._getBucket(ossInfo, endpoint='oss-cn-hangzhou.aliyuncs.com')
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

    def generateUnionID(self, value):
        resultID = self.getMD5String(value)
        return resultID

    def generateCode(self, value):
        code = (hex(int(value)).upper())[2:]
        return code

    def findElement(self, xmlData, tag):
        element = xmlData.find(tag)
        if element is None:
            return ''
        else:
            return element.text

    #获取accessToken, 微信公众号获取用户信息使用
    def getAccessToken(self):
        try:
            now = datetime.datetime.now()
            query = db.session.query(AccessToken)
            result = query.first()
            if result is not None:
                createTime = result.createTime
                validity = result.validity
                intervalTime = validity - (now - createTime).total_seconds()
                accessTokenID = result.accessTokenID
                #如果已经过期，重新请求微信服务器获取
                if intervalTime < INTERVALTIME:
                    query.delete(synchronize_session=False)
                    (status, callBackInfo) = self.__getAccessToken()
                    accessTokenID = callBackInfo['accessTokenID']
                    validity = callBackInfo['validity']
                    accessToken = AccessToken(
                        accessTokenID=accessTokenID, createTime=now, validity=validity
                    )
                    db.session.add(accessToken)
                    db.session.commit()
                    return (True, accessTokenID)
                else:
                    return (True, result.accessTokenID)
            else:
                (status, callBackInfo) = self.__getAccessToken()
                accessTokenID = callBackInfo['accessTokenID']
                validity = callBackInfo['validity']
                accessToken = AccessToken(
                    accessTokenID=accessTokenID, createTime=now, validity=validity
                )
                db.session.add(accessToken)
                db.session.commit()
                return (True, accessTokenID)

        except Exception as e:
            print e
            errorInfo = ErrorInfo['SPORTS_02']
            errorInfo['detail'] = str(e)
            db.session.rollback()
            return (False, errorInfo)

    def __getAccessToken(self):
        postUrl = ("https://api.weixin.qq.com/cgi-bin/token?grant_type="
                   "client_credential&appid=%s&secret=%s" % (PUBLICAPPID, PUBLICSECRET))
        urlResp = urllib.urlopen(postUrl)
        urlResp = json.loads(urlResp.read())
        callBackInfo = {}
        callBackInfo['accessTokenID'] = urlResp['access_token']
        callBackInfo['validity'] = urlResp['expires_in']
        return (True, callBackInfo)



    def parseXmlData(self, xmlData):
        if len(xmlData) == 0:
            return (False, None)
        else:
            xmlData = ET.fromstring(xmlData)
            messageInfo = {}
            messageInfo['toUserName'] = ((xmlData.find('ToUserName') is not None) and xmlData.find('ToUserName').text)
            messageInfo['fromUserName'] = ((xmlData.find('FromUserName') is not None) and xmlData.find('FromUserName').text)
            messageInfo['createTime'] = ((xmlData.find('CreateTime') is not None) and xmlData.find('CreateTime').text)
            messageInfo['megType'] = ((xmlData.find('MsgType') is not None) and xmlData.find('MsgType').text)
            messageInfo['msgId'] = ((xmlData.find('MsgId') is not None) and xmlData.find('MsgId').text)
            messageInfo['content'] = ((xmlData.find('Content') is not None) and xmlData.find('Content').text)
            messageInfo['event'] = ((xmlData.find('Event') is not None) and xmlData.find('Event').text)
            return (True, messageInfo)

    def sendTextMessage(self, info):
        sendInfo = {}
        sendInfo['ToUserName'] = info['fromUserName']
        sendInfo['FromUserName'] = info['toUserName']
        sendInfo['CreateTime'] = int(time.time())
        sendInfo['Content'] = info['content']
        XmlForm = """
        <xml>
        <ToUserName><![CDATA[{ToUserName}]]></ToUserName>
        <FromUserName><![CDATA[{FromUserName}]]></FromUserName>
        <CreateTime>{CreateTime}</CreateTime>
        <MsgType><![CDATA[text]]></MsgType>
        <Content><![CDATA[{Content}]]></Content>
        </xml>
        """
        return XmlForm.format(**sendInfo)



if __name__ == '__main__':
    u = Util()
    print u.generateID('a')
    # print u.isTokenValid('2016-04-22154653e39f5af713d36a703d02e5516c45a565')
