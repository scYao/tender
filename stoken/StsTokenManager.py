# coding=utf8
#标准库导入
import sys

from tool.config import ErrorInfo

reload(sys)
sys.setdefaultencoding('utf-8')
sys.path.append('..')
from  datetime import datetime
import xmltodict
import traceback
import json
from tool.Util import Util
from models.flask_app import db
from models.StsToken import StsToken
from aliyunsdkcore import client
from aliyunsdksts.request.v20150401 import AssumeRoleRequest

from dateutil import tz
from datetime import datetime

class StsTokenManager(Util):
    def __init__(self):
        self.stsAccessKeyID = 'LTAImKuptPCdzEDX'
        self.stsAccessKeySecret = 'OH4e5QvhOHdI5jlWDa1YsW9heRTrVg'
        self.regionId = 'cn-hangzhou'

    def createStsToken(self):

        clt = client.AcsClient(self.stsAccessKeyID, self.stsAccessKeySecret, self.regionId)
        # clt = client.AcsClient('HReEC1sQufBRLcQC', '5rqWY7jXhGeF0HBhYpl10mSkgrrHZt', 'cn-hangzhou')
        request = AssumeRoleRequest.AssumeRoleRequest()
        # 指定角色
        request.set_RoleArn('acs:ram::1406019938967626:role/tenderputrole')
        # 设置会话名称，审计服务使用此名称区分调用者
        request.set_RoleSessionName('tenderPutRole')

        # 发起请求，并得到response
        response = clt.do_action(request)

        info = xmltodict.parse(response)
        AssumeRoleResponse = info['AssumeRoleResponse']
        Credentials = AssumeRoleResponse['Credentials']
        AccessKeySecret = Credentials['AccessKeySecret']
        AccessKeyId = Credentials['AccessKeyId']
        Expiration = Credentials['Expiration']
        SecurityToken = Credentials['SecurityToken']
        now = datetime.now()

        tokenID = self.generateID(SecurityToken)

        # UTC 转换为 本地时间
        # UTC Zone
        from_zone = tz.gettz('UTC')
        # China Zone
        to_zone = tz.gettz('CST')

        utc = datetime.strptime(str(Expiration).replace('T', ' ').replace('Z', ''), "%Y-%m-%d %H:%M:%S")
        utc = utc.replace(tzinfo=from_zone)

        # Convert time zone
        local = utc.astimezone(to_zone)
        local = datetime.strftime(local, "%Y-%m-%d %H:%M:%S")


        try:
            db.session.query(StsToken).delete(synchronize_session=False)
            stsToken = StsToken(tokenID=tokenID, AccessKeySecret=AccessKeySecret, AccessKeyId=AccessKeyId,
                                Expiration=local, SecurityToken=SecurityToken, createTime=now)
            db.session.add(stsToken)
            db.session.commit()
        except Exception as e:
            print e
            traceback.print_exc()
            errorInfo = ErrorInfo['TENDER_02']
            errorInfo['detail'] = str(e)
            db.session.rollback()
            return (False, errorInfo)

    # 获取sts token信息
    def getStsTokenInfo(self, jsonInfo):
        info = json.loads(jsonInfo)
        tokenID = info['tokenID']
        (status, userID) = self.isTokenValid(tokenID)
        if status is not True:
            errorInfo = ErrorInfo['TENDER_01']
            return (False, errorInfo)


        try:
            query = db.session.query(StsToken)
            result = query.first()
            if result is None:
                return (False, ErrorInfo['TENDER_38'])
            dataInfo = StsToken.generate(o=result)
            return (True, dataInfo)
        except Exception as e:
            print e
            traceback.print_exc()
            errorInfo = ErrorInfo['TENDER_02']
            errorInfo['detail'] = str(e)
            db.session.rollback()
            return (False, errorInfo)

if __name__ == '__main__':
    s = StsTokenManager()
    s.createStsToken()

    # s = '''<?xml version='1.0' encoding='UTF-8'?><AssumeRoleResponse><RequestId>57C67914-8894-4C5F-BA76-F79FFBE856D2</RequestId><AssumedRoleUser><AssumedRoleId>338927493372061897:tenderPutRole</AssumedRoleId><Arn>acs:ram::1406019938967626:role/tenderputrole/tenderPutRole</Arn></AssumedRoleUser><Credentials><AccessKeySecret>5N5GPh6SR3m18sjskj826tAFxJ4fy3FssdFH1oByTeZB</AccessKeySecret><AccessKeyId>STS.K2TEinRWBDMZqGQsb6q6iZJGu</AccessKeyId><Expiration>2017-05-02T09:36:09Z</Expiration><SecurityToken>CAIS+QF1q6Ft5B2yfSjIqvHhDtPav4hj84+xc2Hgl2JjfblFtY/slzz2IHtEdXNvBeEdtfs1nG5R5vcdlqRvRplJSFb8cNdK6ZBaqdBymiYV+J7b16cNrbH4M0rxYkeJ8a2/SuH9S8ynCZXJQlvYlyh17KLnfDG5JTKMOoGIjpgVBbZ+HHPPD1x8CcxROxFppeIDKHLVLozNCBPxhXfKB0ca0WgVy0EHsPjnnJXFu0uF3AyklbFP+b6ceMb0M5NeW75kSMqw0eBMca7M7TVd8RAi9t0t1/wVo2ib74rGXAMJvUzWYrXOl8FiKgN0fLAnB7RDqPXsN1WZakxjQO4agAFclE2IAFTF5xoT8J0DNEwndhoE8/ouFjljIKAvvo2x8XWW7fI1M9SuPPoEQvSjKCsBuO04UwbIJhypOUx8sd+bka9dJVCQqJunraiHRpC4W4M9YAnNtJQN5WM5NLp536MQKxPU7vCLDAzpZ62e6uYTf6dPDp+cwDrXQ3f7tX5pZw==</SecurityToken></Credentials></AssumeRoleResponse>'''
    # info = xmltodict.parse(s)
    # AssumeRoleResponse = info['AssumeRoleResponse']
    # Credentials = AssumeRoleResponse['Credentials']
    # AccessKeySecret = Credentials['AccessKeySecret']
    # AccessKeyId = Credentials['AccessKeyId']
    # Expiration = Credentials['Expiration']
    # SecurityToken = Credentials['SecurityToken']
    #
    # from dateutil import tz
    # from datetime import datetime
    #
    # # UTC Zone
    # from_zone = tz.gettz('UTC')
    # # China Zone
    # to_zone = tz.gettz('CST')
    #
    # utc = datetime.utcnow()
    # print utc
    # print str(Expiration).replace('T', ' ').replace('Z', '')
    #
    #
    # # Tell the datetime object that it's in UTC time zone
    # utc = datetime.strptime(str(Expiration).replace('T', ' ').replace('Z', ''), "%Y-%m-%d %H:%M:%S")
    # utc = utc.replace(tzinfo=from_zone)
    #
    # # Convert time zone
    # local = utc.astimezone(to_zone)
    # print datetime.strftime(local, "%Y-%m-%d %H:%M:%S")