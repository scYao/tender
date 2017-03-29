# coding=utf8
import sys

IMAGE_TAG_COMPANY_CERTIFICATION = 1
IMAGE_TAG_COMPANY_LICENSE = 2
IMAGE_TAG_COMPANY_SAFE = 3
IMAGE_TAG_COMPANY_CREDIT = 4

# 关键字 tag
SEARCH_KEY_TAG_USER = 1
SEARCH_KEY_TAG_TENDRE = 2
SEARCH_KEY_TAG_WIN_BIDDING = 3
SEARCH_KEY_TAG_COMPANY = 4 # 企业数据库
SEARCH_KEY_TAG_PROJECT_MANAGER = 5 # 项目经理

FAVORITE_TAG_TENDER = '1'
FAVORITE_TAG_WIN_BIDDING = '2'

#用户类型ID '身份, 1 审定人, 2 审核人, 3 负责人, 4 经办人'
USER_TAG_BOSS = 1
USER_TAG_AUDITOR = 2
USER_TAG_RESPONSIBLEPERSON = 3
USER_TAG_OPERATOR = 4
USER_TAG_DIC = {
    1: '审定人',
    2: '审核人',
    3: '负责人',
    4: '经办人'
}

# 消息类型
MESSAGE_TAG_PUSH = 1 # 推送消息
MESSAGE_TAG_OPERATOR = 2 # 成功分配经办人
#添加消息场景，
# 1,推送消息　create_pushed_tender_by_operator

# 创建经办人, 是否同意
OPERATOR_TAG_CREATED = 0
OPERATOR_TAG_YES = 1
OPERATOR_TAG_NO = 2


#'0表示未开始，１表示正在进行中，２表示已经完成，３表示历史记录',
DOING_STEP = 1
DONE_STEP = 2
HISTORY_STEP = 3

# 决定是否投标
PUSH_TENDER_INFO_TAG_STATE_UNREAD = 0
PUSH_TENDER_INFO_TAG_STATE_APPROVE = 1
PUSH_TENDER_INFO_TAG_STATE_DISCARD = 2

# 标的状态
PUSH_TENDER_INFO_TAG_STEP_WAIT = 0
PUSH_TENDER_INFO_TAG_STEP_DOING = 1
PUSH_TENDER_INFO_TAG_STEP_DONE = 2
PUSH_TENDER_INFO_TAG_STEP_HISTORY = 3


# 代办事项 报名 打保证金 标书 投标
OPERATION_TAG_ENLIST = 1   # 报名
OPERATION_TAG_DEPOSIT = 2   # 打保证金
OPERATION_TAG_MAKE_BIDDING_BOOK = 3   # 制作标书
OPERATION_TAG_ATTEND = 4   # 现场开标

#标书OSS目录
BID_DOC_DIRECTORY = 'biddocument'

#公司ID
CUSTOMIZEDCOMPANYID = '1'

#新建员工默认密码
DEFAULT_PWD = '123456'




