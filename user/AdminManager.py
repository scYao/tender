# coding=utf8
import sys
import urllib2
import poster
import requests

from src.stoken.TokenManager import TokenManager
from src.tool.config import ErrorInfo

sys.path.append("..")
from tool.Util import Util
import json
import os,sys
reload(sys)
sys.setdefaultencoding('utf-8')
#后台管理引用
import hashlib
import json
from sqlalchemy import desc, func, and_, or_
from datetime import datetime
from models.flask_app import db
from models.AdminInfo import AdminInfo


class AdminManager(Util):

    def __init__(self):
        pass

    # 管理员登录
    def adminLogin(self, jsonInfo):
        info = json.loads(jsonInfo)
        adminName = info['adminName']
        password = info['password']

        result = db.session.query(AdminInfo).filter(or_(and_(AdminInfo.adminName==adminName, AdminInfo.adminPW==self.getMD5String(password)),
                                               and_(AdminInfo.tel==adminName, AdminInfo.adminPW==self.getMD5String(password)))).first()

        if result is None:
            errorInfo = ErrorInfo['SPORTS_08']
            errorInfo['detail'] = result
            return (False, errorInfo)
        tokenManager = TokenManager()
        tokenID = tokenManager.createTokenChemy(result.adminID)
        return (True, tokenID)

    # 创建管理员
    def createAdmin(self, jsonInfo):
        info = json.loads(jsonInfo)
        adminName = info['adminName']
        password = info['password']
        tel = info['tel']

        # 查询用户名或手机号是否已经存在
        allResult = db.session.query(AdminInfo).filter(or_(AdminInfo.adminName==adminName,
                                               AdminInfo.tel==tel)).all()
        if len(allResult)>0:
            errorInfo = ErrorInfo['SPORTS_07']
            errorInfo['detail'] = allResult
            return (False, errorInfo)

        adminID = self.generateID(tel)
        admin = AdminInfo(adminID, adminName, self.getMD5String(password), tel)
        db.session.add(admin)
        try:
            db.session.commit()
        except Exception as e:
            print e
            errorInfo = ErrorInfo['SPORTS_02']
            errorInfo['detail'] = e
            db.session.rollback()
            return (False, errorInfo)

        return (True, adminID)

    # 管理员身份验证, 如果身份校验成功,返回管理员ID
    def adminAuth(self, jsonInfo):
        info = json.loads(jsonInfo)
        tokenID = info['tokenID']
        (status, reason) = self.isTokenValid(tokenID)
        if status is not True:
            return (False, reason)

        userID = reason
        # 该userID是否是管理员
        result = db.session.query(AdminInfo).filter(AdminInfo.adminID==userID).first()
        if result is None:
            errorInfo = ErrorInfo['SPORTS_10']
            errorInfo['detail'] = result
            return (False, errorInfo)

        return (True, userID)


if __name__ == '__main__':
    admin = AdminManager()
    info = {}
    # info['tokenID'] = '04a92b12054b6e14e5918b9f21239884'
    info['adminName'] = 'dyw'
    info['password'] = '123456'
    info['tel'] = '18351801163'
    # print admin.adminLogin(json.dumps(info))
    print admin.createAdmin(json.dumps(info))