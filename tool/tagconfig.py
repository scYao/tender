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
SEARCH_KEY_TAG_SUBSCRIBE = 6 #订阅

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
#添加消息场景，
# 1,推送消息　create_pushed_tender_by_operator, create_pushed_tender_by_resp, create_pushed_tender_by_auditor,
#create_pushed_tender_by_boss
MESSAGE_PUSH_DIC = {
    'title': '推送消息',
    4: USER_TAG_RESPONSIBLEPERSON,
    3: USER_TAG_AUDITOR,
    2: USER_TAG_BOSS,
    1: USER_TAG_BOSS,
    'description': '推送了一条新的消息',
    'tag': 1
}

MESSAGE_ASSIGN_DIC = {
    'title': '分配消息',
    3: USER_TAG_BOSS,
    1: USER_TAG_RESPONSIBLEPERSON,
    'description': '新的分配消息',
    'tag': 1
}


# 创建经办人, 是否同意
OPERATOR_TAG_CREATED = 0
OPERATOR_TAG_YES = 1
OPERATOR_TAG_NO = 2

#公众号ID, Secret
PUBLICAPPID = 'wx6b06cac8fee40771'
PUBLICSECRET = 'd6e12e186ec9e1dbf756f5cb3395b622'
INTERVALTIME = 100


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

# 自定义标 原生标
PUSH_TENDER_INFO_TAG_TENDER = 0
PUSH_TENDER_INFO_TAG_CUS = 1

# 代办事项 报名 打保证金 标书 投标
# 改为 确定投标价格，保证金支付，投标方案，标书制作，项目经理安排
# 修改为 报名工作 投标保证金 开标人确认 标书制作
OPERATION_TAG_ENLIST = 1   # 确定投标价格
OPERATION_TAG_DEPOSIT = 2   # 保证金支付
OPERATION_TAG_CONFIRM_USER = 3   # 投标方案 OPERATION_TAG_MAKE_BIDDING_BOOK
OPERATION_TAG_MAKE_BIDDING_BOOK = 4   # 标书制作
# OPERATION_TAG_MANAGER_ARRANGEMENT = 5   # 项目经理安排

#标书OSS目录
BID_DOC_DIRECTORY = 'biddocument'
CUS_TENDER_DOC_DIRECTORY = 'customizedtender'
TENDER_NEWS = 'tendernews'

#公司ID
CUSTOMIZEDCOMPANYID = '1'

#新建员工默认密码
DEFAULT_PWD = '123456'

BIDDING_BOOK_BUSINESS = 1
BIDDING_BOOK_TECHNIQUE = 2

#==============
#公众号信息
TEMPLATEID = 'mVigPJBbCfdPJrmT2CLqk_Rv8uD_JYBhirsu2-oGJFE'#模板ID
MINIAPPID = 'wx3f8eb38c63060bf4' #小程序ID


RIGHT_TAG_CONTRACT = 1