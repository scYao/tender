# coding=utf8
ErrorInfo = {}

ErrorInfo['TENDER_01'] = {
    'code' : 'TENDER_01',
    'info' : 'Bad token',
    'zhInfo' : '登录过期'
}

ErrorInfo['TENDER_02'] = {
    'code' : 'TENDER_02',
    'info' : 'sql error',
    'zhInfo' : 'sql语句错误'
}

ErrorInfo['TENDER_03'] = {
    'code' : 'TENDER_03',
    'info' : 'no result',
    'zhInfo' : '没有数据'
}

ErrorInfo['TENDER_04'] = {
    'code' : 'TENDER_04',
    'info' : 'tender id is null',
    'zhInfo' : 'tenderID无效!'
}

ErrorInfo['TENDER_05'] = {
    'code' : 'TENDER_05',
    'info' : 'wrong password',
    'zhInfo' : '密码错误!'
}

ErrorInfo['TENDER_06'] = {
    'code' : 'TENDER_06',
    'info' : 'sms code invalid!',
    'zhInfo' : '验证码错误!'
}

ErrorInfo['TENDER_07'] = {
    'code' : 'TENDER_07',
    'info' : 'user already exists',
    'zhInfo' : '用户已存在!'
}

ErrorInfo['TENDER_08'] = {
    'code' : 'TENDER_08',
    'info' : 'get max type1 id error',
    'zhInfo' : '获取最大type1类型错误!'
}

ErrorInfo['TENDER_09'] = {
    'code' : 'TENDER_09',
    'info' : 'no such user',
    'zhInfo' : 'userID 错误!'
}

ErrorInfo['TENDER_10'] = {
    'code' : 'TENDER_10',
    'info' : 'tel not exists',
    'zhInfo' : '手机号不存在!'
}

ErrorInfo['TENDER_11'] = {
    'code' : 'TENDER_11',
    'info' : 'sms code error!',
    'zhInfo' : '验证码无效!'
}

ErrorInfo['TENDER_12'] = {
    'code' : 'TENDER_12',
    'info' : 'already create favorite!',
    'zhInfo' : '已经收藏!'
}


ErrorInfo['TENDER_13'] = {
    'code' : 'TENDER_13',
    'info' : 'name or password error!',
    'zhInfo' : '用户名或密码错误!'
}

ErrorInfo['TENDER_14'] = {
    'code' : 'TENDER_14',
    'info' : 'admin auth error!',
    'zhInfo' : '管理员身份验证错误!'
}

ErrorInfo['TENDER_15'] = {
    'code' : 'TENDER_15',
    'info' : 'tender already exists!',
    'zhInfo' : '该标段已存在!'
}

ErrorInfo['TENDER_16'] = {
    'code' : 'TENDER_16',
    'info' : 'candidate already exists!',
    'zhInfo' : '该候选人已存在!'
}

ErrorInfo['TENDER_17'] = {
    'code' : 'TENDER_17',
    'info' : 'win bidding already exists!',
    'zhInfo' : '该中标已存在!'
}

ErrorInfo['TENDER_18'] = {
    'code' : 'TENDER_18',
    'info' : 'company already exists!',
    'zhInfo' : '该公司已存在!'
}

ErrorInfo['TENDER_19'] = {
    'code' : 'TENDER_19',
    'info' : 'project manager already exists!',
    'zhInfo' : '该项目经理已存在!'
}

ErrorInfo['TENDER_20'] = {
    'code' : 'TENDER_20',
    'info' : 'project manager achievement already exists!',
    'zhInfo' : '该项目经理业绩已存在!'
}

ErrorInfo['TENDER_21'] = {
    'code' : 'TENDER_21',
    'info' : 'company achievement already exists!',
    'zhInfo' : '该公司业绩已存在!'
}

ErrorInfo['TENDER_22'] = {
    'code' : 'TENDER_22',
    'info' : 'company delinquenent conduct already exists!',
    'zhInfo' : '该不良行为已存在!'
}

ErrorInfo['TENDER_23'] = {
    'code' : 'TENDER_23',
    'info' : 'user does not exists!',
    'zhInfo' : '该用户不存在!'
}

ErrorInfo['TENDER_24'] = {
    'code' : 'TENDER_24',
    'info' : 'can not create operator!',
    'zhInfo' : '只有负责人才能创建经办人!'
}

ErrorInfo['TENDER_25'] = {
    'code' : 'TENDER_25',
    'info' : 'the pushed tender info already exist!',
    'zhInfo' : '招标公告已经推送'
}

ErrorInfo['TENDER_26'] = {
    'code' : 'TENDER_26',
    'info' : 'the operator is not exist!',
    'zhInfo' : '不存在经办人'
}

ErrorInfo['TENDER_27'] = {
    'code' : 'TENDER_27',
    'info' : 'you are not the right operator!',
    'zhInfo' : '不是经办人，无法填写'
}

ErrorInfo['TENDER_28'] = {
    'code' : 'TENDER_28',
    'info' : 'the pushed tender info is not exist',
    'zhInfo' : '推送消息不存在'
}

ErrorInfo['TENDER_29'] = {
    'code' : 'TENDER_29',
    'info' : 'you have create quoted price!',
    'zhInfo' : '已经填写了报价信息'
}

ErrorInfo['TENDER_30'] = {
    'code' : 'TENDER_30',
    'info' : 'update pushed tender info step error!',
    'zhInfo' : '更新进度失败'
}

ErrorInfo['TENDER_31'] = {
    'code' : 'TENDER_31',
    'info' : 'upload file error!',
    'zhInfo' : '上传文件错误'
}

ErrorInfo['TENDER_32'] = {
    'code' : 'TENDER_32',
    'info' : 'get operator error!',
    'zhInfo' : '获取经办人失败'
}

ErrorInfo['TENDER_33'] = {
    'code' : 'TENDER_33',
    'info' : 'can not delete other company\'s user !',
    'zhInfo' : '无法删除其他公司的用户!'
}

ErrorInfo['TENDER_34'] = {
    'code' : 'TENDER_34',
    'info' : 'user is not oa user!',
    'zhInfo' : '用户不是OA用户!'
}


#支付宝公钥
ALIPAY_PUBLIC_KEY = '''-----BEGIN PUBLIC KEY-----\n
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCnxj/9qwVfgoUh/y2W89L6BkRA\n
FljhNhgPdyPuBV64bfQNN1PjbCzkIM6qRdKBoLPXmKKMiFYnkd6rAoprih3/PrQE\n
B/VsW8OoM8fxn67UDYuyBTqA23MML9q1+ilIZwBC2AQ2UBVOrFXfFl75p6/B5Ksi\n
NG9zpgmLCUYuLkxpLQIDAQAB\n
-----END PUBLIC KEY-----'''


WHOOSH_BASE = '../../smartsearchData/'
# WHOOSH_BASE = '/home/yz/work/tenderSearchKey/'
# WHOOSH_BASE = '/opt/smartsearchData/'
# WHOOSH_BASE = '/Users/zhushijie/Documents/Server/smartsearchData/'


