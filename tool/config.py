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


#支付宝公钥
ALIPAY_PUBLIC_KEY = '''-----BEGIN PUBLIC KEY-----\n
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCnxj/9qwVfgoUh/y2W89L6BkRA\n
FljhNhgPdyPuBV64bfQNN1PjbCzkIM6qRdKBoLPXmKKMiFYnkd6rAoprih3/PrQE\n
B/VsW8OoM8fxn67UDYuyBTqA23MML9q1+ilIZwBC2AQ2UBVOrFXfFl75p6/B5Ksi\n
NG9zpgmLCUYuLkxpLQIDAQAB\n
-----END PUBLIC KEY-----'''


WHOOSH_BASE =  '/home/yz/work/smartsearchData/'
# WHOOSH_BASE = '/opt/smartsearchData/'
# WHOOSH_BASE = '/Users/zhushijie/Documents/Server/smartsearchData/'


