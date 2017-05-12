# coding=utf8
import sys
import json


sys.path.append("..")
import os, random, requests
reload(sys)
sys.setdefaultencoding('utf-8')

from datetime import datetime
from sqlalchemy import and_, text, func, desc

from models.flask_app import db
from models.Operator import Operator
from models.Message import Message
from models.PushedTenderInfo import PushedTenderInfo
from models.TenderComment import TenderComment
from tool.Util import Util
from tool.config import ErrorInfo
from tool.tagconfig import OPERATOR_TAG_CREATED, DOING_STEP, DONE_STEP, HISTORY_STEP, PUSH_TENDER_INFO_TAG_CUS, \
    PUSH_TENDER_INFO_TAG_TENDER, OPERATOR_TAG_YES, PUSH_TENDER_INFO_TAG_STEP_DOING
from tool.tagconfig import USER_TAG_OPERATOR, USER_TAG_RESPONSIBLEPERSON, USER_TAG_AUDITOR, USER_TAG_BOSS
from pushedTender.TenderCommentManager import TenderCommentManager

from pushedTender.PushedTenderManager import PushedTenderManager
from user.UserBaseManager import UserBaseManager
from user.UserManager import UserManager
from tender.CustomizedTenderManager import CustomizedTenderManager
from department.DepartmentManager import DepartmentManager
from department.DepartmentAreaManager import DepartmentAreaManager
from department.DepartmentRightManager import DepartmentRightManager


class BossManager(UserBaseManager):

    def __init__(self):
        pass

    # 审定人创建推送
    def createPushedTenderByBoss(self, jsonInfo):
        info = json.loads(jsonInfo)
        info['userType'] = USER_TAG_BOSS
        (status, userID) = PushedTenderManager.isTokenValidByUserType(info=info)
        if status is not True:
            errorInfo = ErrorInfo['TENDER_01']
            return (False, errorInfo)
        info['tag'] = USER_TAG_BOSS
        info['userID'] = userID
        info['pushedTenderInfoTag'] = PUSH_TENDER_INFO_TAG_TENDER
        pushedTenderManager = PushedTenderManager()
        return pushedTenderManager.createPushedTender(info=info)

    # 审定人取消推送
    def deletePushedTenderByBoss(self, jsonInfo):
        info = json.loads(jsonInfo)
        info['userType'] = USER_TAG_BOSS
        (status, userID) = PushedTenderManager.isTokenValidByUserType(info=info)
        if status is not True:
            errorInfo = ErrorInfo['TENDER_01']
            return (False, errorInfo)
        info['userID'] = userID
        pushedTenderManager = PushedTenderManager()
        return pushedTenderManager.deletePushedTender(info=info)

    # 创建推送, 自定义标
    def createCustomizedTenderByBoss(self, jsonInfo, imgFileList):
        info = json.loads(jsonInfo)
        info['userType'] = USER_TAG_OPERATOR
        (status, userID) = PushedTenderManager.isTokenValidByUserType(info=info)
        if status is not True:
            errorInfo = ErrorInfo['TENDER_01']
            return (False, errorInfo)
        info['userID'] = userID
        customizedTenderManager = CustomizedTenderManager()
        (status, tenderID) = customizedTenderManager.createCustomizedTender(info=info, imgFileList=imgFileList)
        info['tenderID'] = tenderID
        pushedTenderManager = PushedTenderManager()
        info['pushedTenderInfoTag'] = PUSH_TENDER_INFO_TAG_CUS
        return pushedTenderManager.createPushedTender(info)

    # 审定人填写进行中项目的报价信息
    def createQuotedPriceByBoss(self, jsonInfo):
        info = json.loads(jsonInfo)
        info['userType'] = USER_TAG_BOSS
        (status, userID) = PushedTenderManager.isTokenValidByUserType(info=info)
        if status is not True:
            errorInfo = ErrorInfo['TENDER_01']
            return (False, errorInfo)
        info['userID'] = userID
        pushedTenderManager = PushedTenderManager()
        return pushedTenderManager.createQuotedPrice(info=info)

    # 审定人批注正在进行中的项目
    def createTenderCommentByBoss(self, jsonInfo):
        info = json.loads(jsonInfo)
        info['userType'] = USER_TAG_BOSS
        (status, userID) = PushedTenderManager.isTokenValidByUserType(info=info)
        if status is not True:
            errorInfo = ErrorInfo['TENDER_01']
            return (False, errorInfo)
        info['userID'] = userID
        tenderCommentManager = TenderCommentManager()
        return tenderCommentManager.createTenderComment(info=info)


    # 审定人删除批注
    def deleteTenderCommentByBoss(self, jsonInfo):
        info = json.loads(jsonInfo)
        info['userType'] = USER_TAG_BOSS
        (status, userID) = PushedTenderManager.isTokenValidByUserType(info=info)
        if status is not True:
            errorInfo = ErrorInfo['TENDER_01']
            return (False, errorInfo)
        info['userID'] = userID
        tenderCommentManager = TenderCommentManager()
        return tenderCommentManager.deleteTenderComment(info=info)

    # 决定是否投标
    def operatePushedTenderInfo(self, jsonInfo):
        info = json.loads(jsonInfo)
        info['userType'] = USER_TAG_BOSS
        (status, userID) = PushedTenderManager.isTokenValidByUserType(info=info)
        if status is not True:
            errorInfo = ErrorInfo['TENDER_01']
            return (False, errorInfo)
        pushedTenderManager = PushedTenderManager()
        info['userType'] = USER_TAG_BOSS
        info['userID'] = userID
        return pushedTenderManager.updatePushedTenderInfo(info=info)

    # 决定是否采用该经办人
    def validateOperator(self, jsonInfo):
        info = json.loads(jsonInfo)
        info['userType'] = USER_TAG_BOSS
        (status, userID) = PushedTenderManager.isTokenValidByUserType(info=info)
        if status is not True:
            errorInfo = ErrorInfo['TENDER_01']
            return (False, errorInfo)
        pushedTenderManager = PushedTenderManager()
        info['userType'] = USER_TAG_BOSS
        return pushedTenderManager.validateOperator(info=info)

    # 老板确定推送消息后,  获取推送消息列表
    def getCertainPushedList(self, jsonInfo):
        pass

    # 审定人 获取负责人推送列表
    def getRespPushedListByBoss(self, jsonInfo):
        info = json.loads(jsonInfo)
        info['userType'] = USER_TAG_BOSS
        (status, userID) = PushedTenderManager.isTokenValidByUserType(info=info)
        if status is not True:
            errorInfo = ErrorInfo['TENDER_01']
            return (False, errorInfo)
        info['userID'] = userID
        pushedTenderManager = PushedTenderManager()
        # 此方法同 负责人获取我的推送 所以此处伪装成负责人
        info['userType'] = USER_TAG_RESPONSIBLEPERSON
        return pushedTenderManager.getPushedTenderListByUserType(info=info)

    # 审定人获取 审核人的推送列表
    def getAuditorPushedListByBoss(self, jsonInfo):
        info = json.loads(jsonInfo)
        info['userType'] = USER_TAG_BOSS
        (status, userID) = PushedTenderManager.isTokenValidByUserType(info=info)
        if status is not True:
            errorInfo = ErrorInfo['TENDER_01']
            return (False, errorInfo)
        info['userType'] = USER_TAG_AUDITOR
        pushedTenderManager = PushedTenderManager()
        return pushedTenderManager.getPushedTenderListByUserType(info=info)

    # 审定人 获取某个经办人的推送列表
    def getOperatorPushedListByBoss(self, jsonInfo):
        info = json.loads(jsonInfo)
        tokenID = info['tokenID']
        operatorUserID = info['userID']
        (status, userID) = self.isTokenValid(tokenID)
        if status is not True:
            errorInfo = ErrorInfo['TENDER_01']
            return (False, errorInfo)
        info['staffUserID'] = operatorUserID
        pushedTenderManager = PushedTenderManager()
        return pushedTenderManager.getPushedTenderListByUserID(info=info)

    # 审定人  获取所有人的推送列表
    def getAllPushedListByBoss(self, jsonInfo):
        info = json.loads(jsonInfo)
        tokenID = info['tokenID']
        (status, userID) = self.isTokenValid(tokenID)
        if status is not True:
            errorInfo = ErrorInfo['TENDER_01']
            return (False, errorInfo)

        info['selfUserID'] = userID
        info['staffUserID'] = info['userID']
        info['selfUserType'] = USER_TAG_BOSS
        pushedTenderManager = PushedTenderManager()
        return pushedTenderManager.getAllPushedList(info=info)

    # 审定人获取待分配列表
    def getUndistributedTenderListByBoss(self, jsonInfo):
        info = json.loads(jsonInfo)
        info['userType'] = USER_TAG_BOSS
        (status, userID) = PushedTenderManager.isTokenValidByUserType(info=info)
        if status is not True:
            errorInfo = ErrorInfo['TENDER_01']
            return (False, errorInfo)
        pushedTenderManager = PushedTenderManager()
        return pushedTenderManager.getUndistributedTenderList(info=info)

    # 审定人获取已分配列表
    def getDistributedTenderListByBoss(self, jsonInfo):
        info = json.loads(jsonInfo)
        info['userType'] = USER_TAG_BOSS
        (status, userID) = PushedTenderManager.isTokenValidByUserType(info=info)
        if status is not True:
            errorInfo = ErrorInfo['TENDER_01']
            return (False, errorInfo)
        pushedTenderManager = PushedTenderManager()
        return pushedTenderManager.getDistributedTenderList(info=info)


    # 审定人获取 正在进行中的招标详情
    def getDoingDetailByBoss(self, jsonInfo):
        info = json.loads(jsonInfo)
        info['userType'] = USER_TAG_BOSS
        (status, userID) = PushedTenderManager.isTokenValidByUserType(info=info)
        if status is not True:
            errorInfo = ErrorInfo['TENDER_01']
            return (False, errorInfo)
        pushedTenderManager = PushedTenderManager()
        info['userID'] = userID
        return pushedTenderManager.getTenderDoingDetail(info=info)


    #账号管理,获取员工列表
    def getUserInfoListByBoss(self, jsonInfo):
        info = json.loads(jsonInfo)
        info['userType'] = USER_TAG_BOSS
        (status, userID) = PushedTenderManager.isTokenValidByUserType(info=info)
        if status is not True:
            errorInfo = ErrorInfo['TENDER_01']
            return (False, errorInfo)
        userManager = UserManager()
        return userManager.getOAUserInfoList(info=info)

    # 审定人获取推送人员列表
    def getTenderUserInfoListByBoss(self, jsonInfo):
        info = json.loads(jsonInfo)
        info['userType'] = USER_TAG_BOSS
        (status, userID) = PushedTenderManager.isTokenValidByUserType(info=info)
        if status is not True:
            errorInfo = ErrorInfo['TENDER_01']
            return (False, errorInfo)
        userManager = UserManager()
        info['userID'] = userID
        (status, userInfo) = self.getUserInfo(info=info)
        info['customizedCompanyID'] = userInfo['customizedCompanyID']
        return userManager.getTenderUserInfoList(info=info)

    #账号管理，创建新员工
    def createUserInfoByBoss(self, jsonInfo):
        info = json.loads(jsonInfo)
        info['OAUserType'] = info['userTypeID']
        info['userType'] = USER_TAG_BOSS
        (status, userID) = PushedTenderManager.isTokenValidByUserType(info=info)
        if status is not True:
            errorInfo = ErrorInfo['TENDER_01']
            return (False, errorInfo)
        userManager = UserManager()
        info['bossUserID'] = userID
        return userManager.createOAUserInfo(info=info)

    #账号管理，修改员工信息
    def updateUserInfoByBoss(self, jsonInfo):
        info = json.loads(jsonInfo)
        info['OAUserType'] = info['userTypeID']
        info['userType'] = USER_TAG_BOSS
        (status, userID) = PushedTenderManager.isTokenValidByUserType(info=info)
        if status is not True:
            errorInfo = ErrorInfo['TENDER_01']
            return (False, errorInfo)
        userManager = UserManager()
        info['bossUserID'] = userID
        return userManager.updateOAUserInfo(info=info)

    # 审定人获取某个员工的信息
    def getUserInfoByBoss(self, jsonInfo):
        info = json.loads(jsonInfo)
        info['userType'] = USER_TAG_BOSS
        (status, userID) = PushedTenderManager.isTokenValidByUserType(info=info)
        if status is not True:
            errorInfo = ErrorInfo['TENDER_01']
            return (False, errorInfo)
        return self.getUserInfo(info=info)

    #账号管理，删除员工
    def deleteUserInfoByBoss(self, jsonInfo):
        info = json.loads(jsonInfo)
        info['userType'] = USER_TAG_BOSS
        (status, userID) = PushedTenderManager.isTokenValidByUserType(info=info)
        if status is not True:
            errorInfo = ErrorInfo['TENDER_01']
            return (False, errorInfo)
        userManager = UserManager()
        info['selfUserID'] = userID
        return userManager.deleteOAUserInfo(info=info)

    # 审定人获取回收站列表
    def getDiscardPushedListByBoss(self, jsonInfo):
        info = json.loads(jsonInfo)
        tokenID = info['tokenID']
        (status, userID) = self.isTokenValid(tokenID)
        if status is not True:
            errorInfo = ErrorInfo['TENDER_01']
            return (False, errorInfo)

        info['selfUserID'] = userID
        info['selfUserType'] = USER_TAG_RESPONSIBLEPERSON
        info['staffUserID'] = '-1'

        pushedTenderManager = PushedTenderManager()
        return pushedTenderManager.getDiscardPushedListWithPushedList(info=info)

    # 从回收站回收
    def recoverPushedTenderByBoss(self, jsonInfo):
        info = json.loads(jsonInfo)
        tokenID = info['tokenID']
        (status, userID) = self.isTokenValid(tokenID)
        if status is not True:
            errorInfo = ErrorInfo['TENDER_01']
            return (False, errorInfo)

        pushedTenderManager = PushedTenderManager()
        return pushedTenderManager.recoverPushedTenderInfo(info=info)

    # 获取所有员工的推送信息
    def getAllDataInfoByBoss(self, jsonInfo):
        info = json.loads(jsonInfo)
        (status, dataInfo) = self.getTenderUserInfoListByBoss(jsonInfo=jsonInfo)
        dataList = dataInfo['dataList']

        pushedTenderManager = PushedTenderManager()
        _ = [self.addPushedDataInfoToUser(o=o, pushedTenderManager=pushedTenderManager, info=info) for o in dataList]
        return (True, dataInfo)

    # 审定人 分配经办人
    def updateOperatorByBoss(self, jsonInfo):
        info = json.loads(jsonInfo)
        info['userType'] = USER_TAG_BOSS
        (status, userID) = PushedTenderManager.isTokenValidByUserType(info=info)
        if status is not True:
            errorInfo = ErrorInfo['TENDER_01']
            return (False, errorInfo)
        # 验证登录
        userID = info['userID']
        tenderID = info['tenderID']
        try:
            # boss 分配人时 直接将人分配，且状态变为进行中
            query = db.session.query(Operator).filter(
                Operator.tenderID == tenderID
            )
            updateInfo = {
                Operator.userID: userID,
                Operator.state : OPERATOR_TAG_YES
            }
            query.update(
                updateInfo, synchronize_session=False
            )

            db.session.query(PushedTenderInfo).filter(
                PushedTenderInfo.tenderID == tenderID
            ).update({
                PushedTenderInfo.step : PUSH_TENDER_INFO_TAG_STEP_DOING
            }, synchronize_session=False)
            db.session.commit()
        except Exception as e:
            print str(e)
            # traceback.print_stack()
            db.session.rollback()
            errorInfo = ErrorInfo['TENDER_02']
            errorInfo['detail'] = str(e)
            return (False, errorInfo)
        return (True, None)

    # 审定人创建标书
    def createOperationBiddingBookByBoss(self, jsonInfo, imgFileList):
        info = json.loads(jsonInfo)
        info['userType'] = USER_TAG_BOSS
        jsonInfo = json.dumps(info)
        return self.createOperationBiddingBook(jsonInfo=jsonInfo, imgFileList=imgFileList)

    # 去使能用户
    def disableUserByBoss(self, jsonInfo):
        info = json.loads(jsonInfo)
        tokenID = info['tokenID']
        (status, userID) = self.isTokenValid(tokenID)
        if status is not True:
            errorInfo = ErrorInfo['TENDER_01']
            return (False, errorInfo)

        paramInfo = {}
        paramInfo['userID'] = userID
        (status, userInfo) = self.getUserInfo(info=paramInfo)
        if status is False:
            return (False, userInfo)

        userType = userInfo['userType']
        if userType != USER_TAG_BOSS:
            return (False, ErrorInfo['TENDER_41'])

        info['disable'] = True
        return self.updateUserDisableInfo(info=info)

    # 是能用户
    def enableUserByBoss(self, jsonInfo):
        info = json.loads(jsonInfo)
        tokenID = info['tokenID']
        (status, userID) = self.isTokenValid(tokenID)
        if status is not True:
            errorInfo = ErrorInfo['TENDER_01']
            return (False, errorInfo)

        paramInfo = {}
        paramInfo['userID'] = userID
        (status, userInfo) = self.getUserInfo(info=paramInfo)
        if status is False:
            return (False, userInfo)

        userType = userInfo['userType']
        if userType != USER_TAG_BOSS:
            return (False, ErrorInfo['TENDER_41'])

        info['disable'] = False
        return self.updateUserDisableInfo(info=info)


    def getDepartmentListByBoss(self, jsonInfo):
        info = json.loads(jsonInfo)
        tokenID = info['tokenID']
        (status, userID) = self.isTokenValid(tokenID)
        if status is not True:
            errorInfo = ErrorInfo['TENDER_01']
            return (False, errorInfo)
        departmentManager = DepartmentManager()
        return departmentManager.getDepartmentList(info=info)

    # 审定人创建部门
    def createDepartmentByBoss(self, jsonInfo):
        info = json.loads(jsonInfo)
        tokenID = info['tokenID']
        (status, userID) = self.isTokenValid(tokenID)
        if status is not True:
            errorInfo = ErrorInfo['TENDER_01']
            return (False, errorInfo)
        departmentManager = DepartmentManager()
        return departmentManager.createDepartment(info=info)

    # 审定人删除部门
    def deleteDepartmentByBoss(self, jsonInfo):
        info = json.loads(jsonInfo)
        tokenID = info['tokenID']
        (status, userID) = self.isTokenValid(tokenID)
        if status is not True:
            errorInfo = ErrorInfo['TENDER_01']
            return (False, errorInfo)
        departmentManager = DepartmentManager()
        return departmentManager.deleteDepartment(info=info)

    # 审定人更新部门信息
    def updateDepartmentByBoss(self, jsonInfo):
        info = json.loads(jsonInfo)
        tokenID = info['tokenID']
        (status, userID) = self.isTokenValid(tokenID)
        if status is not True:
            errorInfo = ErrorInfo['TENDER_01']
            return (False, errorInfo)
        departmentManager = DepartmentManager()
        return departmentManager.updateDepartmentName(info=info)

    # 审定人 获取某个部门的信息
    def getDepartmentByID(self, jsonInfo):
        info = json.loads(jsonInfo)
        tokenID = info['tokenID']
        (status, userID) = self.isTokenValid(tokenID)
        if status is not True:
            errorInfo = ErrorInfo['TENDER_01']
            return (False, errorInfo)
        departmentManager = DepartmentManager()
        return departmentManager.getDepartmentByID(info=info)

    # 审定人 获取某个部门的信息
    def getDepartmentAreaListByBoss(self, jsonInfo):
        info = json.loads(jsonInfo)
        tokenID = info['tokenID']
        (status, userID) = self.isTokenValid(tokenID)
        if status is not True:
            errorInfo = ErrorInfo['TENDER_01']
            return (False, errorInfo)
        departmentAreaManager = DepartmentAreaManager()
        return departmentAreaManager.getAreaListByDepartmentID(info=info)

    # 审定人 创建部门区域
    def createDepartmentAreaByBoss(self, jsonInfo):
        info = json.loads(jsonInfo)
        tokenID = info['tokenID']
        (status, userID) = self.isTokenValid(tokenID)
        if status is not True:
            errorInfo = ErrorInfo['TENDER_01']
            return (False, errorInfo)
        departmentAreaManager = DepartmentAreaManager()
        return departmentAreaManager.createDepartmentArea(info=info)

    # 审定人 删除部门区域
    def deleteDepartmentAreaByBoss(self, jsonInfo):
        info = json.loads(jsonInfo)
        tokenID = info['tokenID']
        (status, userID) = self.isTokenValid(tokenID)
        if status is not True:
            errorInfo = ErrorInfo['TENDER_01']
            return (False, errorInfo)
        departmentAreaManager = DepartmentAreaManager()
        return departmentAreaManager.deleteDepartmentArea(info=info)

    # 审定人 获取指定部门区域
    def getAreaByIDByBoss(self, jsonInfo):
        info = json.loads(jsonInfo)
        tokenID = info['tokenID']
        (status, userID) = self.isTokenValid(tokenID)
        if status is not True:
            errorInfo = ErrorInfo['TENDER_01']
            return (False, errorInfo)
        departmentAreaManager = DepartmentAreaManager()
        return departmentAreaManager.getAreaByID(info=info)

    # 审定人 更新部门区域
    def updateDepartmentAreaNameByBoss(self, jsonInfo):
        info = json.loads(jsonInfo)
        tokenID = info['tokenID']
        (status, userID) = self.isTokenValid(tokenID)
        if status is not True:
            errorInfo = ErrorInfo['TENDER_01']
            return (False, errorInfo)
        departmentAreaManager = DepartmentAreaManager()
        return departmentAreaManager.updateDepartmentAreaName(info=info)


    def getAreaTreeByBoss(self, jsonInfo):
        info = json.loads(jsonInfo)
        tokenID = info['tokenID']
        (status, userID) = self.isTokenValid(tokenID)
        if status is not True:
            errorInfo = ErrorInfo['TENDER_01']
            return (False, errorInfo)
        departmentAreaManager = DepartmentAreaManager()
        return departmentAreaManager.getAreaTree(info=info)

    def getAreaTreeWithoutUserIDByBoss(self, jsonInfo):
        info = json.loads(jsonInfo)
        tokenID = info['tokenID']
        (status, userID) = self.isTokenValid(tokenID)
        if status is not True:
            errorInfo = ErrorInfo['TENDER_01']
            return (False, errorInfo)
        departmentAreaManager = DepartmentAreaManager()
        return departmentAreaManager.getAreaTreeWithoutUserID(info=info)

    # 设置权限
    def createRightByBoss(self, jsonInfo):
        info = json.loads(jsonInfo)
        tokenID = info['tokenID']
        (status, userID) = self.isTokenValid(tokenID)
        if status is not True:
            errorInfo = ErrorInfo['TENDER_01']
            return (False, errorInfo)
        departmentRightManager = DepartmentRightManager()
        return departmentRightManager.createRight(info=info)

    # 取消权限
    def deleteRightByBoss(self, jsonInfo):
        info = json.loads(jsonInfo)
        tokenID = info['tokenID']
        (status, userID) = self.isTokenValid(tokenID)
        if status is not True:
            errorInfo = ErrorInfo['TENDER_01']
            return (False, errorInfo)
        departmentRightManager = DepartmentRightManager()
        return departmentRightManager.deleteRight(info=info)