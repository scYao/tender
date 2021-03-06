# coding=utf8

import urllib2
import urllib
import json
import poster as poster
import sys
import oss2
from test_config import LOCALHOST, PORT, DATA_TEXT_PATH, ADMIN_TOKEN, TYPE1_ID

reload(sys)
sys.setdefaultencoding('utf-8')

from datetime import datetime, timedelta

# 从sql表内容，生成创建时的info解析出的内容
# companyID = info['companyID'].replace('\'', '\\\'').replace('\"', '\\\"')
def sql_to_create_info(info):
    lines = info.split('\n')
    for l in lines:
        str = l.strip()
        words = str.split(' ')
        name = words[0]
        stype = words[1]
        # 只有字符串带replace
        if 'nvarchar' in stype:
            template = "%s = info['%s'].replace(\'\\\'\', \'\\\\\\\'\').replace(\'\\\"\', \'\\\\\\\"\')" % (name, name)
        else:
            template = "%s = info['%s']" % (name, name)
        print template

# create 时, model参数列表
# companyID=companyID, companyName=companyName, newArchiveID=newArchiveID,
# registerArea=registerArea, companyAreaType=companyAreaType, certificateID=certificateID,
# certificationAuthority=certificationAuthority, legalRepresentative=legalRepresentative,
def sql_to_model_init_model_param(info):
    lines = info.split('\n')
    paramList = []
    for l in lines:
        str = l.strip()
        words = str.split(' ')
        name = words[0]

        template = ' %s=%s' % (name, name)
        paramList.append(template)
    print ','.join(paramList)

# 从sql表内容，到model类的成员变量
# companyID = db.Column(db.String(100), primary_key=True)
# companyName = db.Column(db.String(100))
# newArchiveID = db.Column(db.String(100))
# registerArea = db.Column(db.String(100))
# companyAreaType = db.Column(db.String(100))
def sql_to_model_members(info):
    typeDic = {}
    typeDic['nvarchar'] = 'String'
    typeDic['float'] = 'Float'
    typeDic['double'] = 'Float'
    typeDic['text'] = 'Text'
    typeDic['date'] = 'Date'
    typeDic['datetime'] = 'DateTime'
    typeDic['bool'] = 'Boolean'
    typeDic['boolean'] = 'Boolean'
    typeDic['bigint'] = 'BigInteger'
    typeDic['int'] = 'Integer'
    typeDic['smallint'] = 'Integer'

    lines = info.split('\n')
    for l in lines:
        str = l.strip()
        words = str.split(' ')
        name = words[0]
        stype = words[1]
        pri = words[2]
        if pri == 'primary' or pri == 'auto_increment':
            pri = ', primary_key=True'
        else:
            pri = ''

        if 'nvarchar' in stype:
            typeList = stype.split('(')
            t1 = typeDic[typeList[0]]
            t2 = typeList[1][:-1]
            stype = 'db.Column(db.String(%s)%s)' % (t2, pri)

        else:
            stype = 'db.Column(db.%s%s)' % (typeDic[stype], pri)

        template = '%s = %s' % (name, stype)
        print template

# 构造函数
# self.creditFinancialStaff = creditFinancialStaff
# self.companyBrief = companyBrief
#  companyID=None, companyName=None, newArchiveID=None, r
def sql_to_model_init(info):
    lines = info.split('\n')
    paramList = []
    for l in lines:
        str = l.strip()
        words = str.split(' ')
        name = words[0]
        stype = words[1]

        default = 'None'

        try:
            index = words.index('default')
            index = index + 1
            default = words[index]
            print default
        except Exception as e:
            if 'int' in stype or 'float' == stype or 'double' == stype:
                default = '0'
            elif 'bool' == stype:
                default = 'False'
            else:
                default = 'None'


        template = ' %s=%s' % (name, default)
        paramList.append(template)

        print 'self.%s = %s' % (name, name)

    print ','.join(paramList)

# res['companyID'] = o.companyID
# res['companyName'] = o.companyName
# res['newArchiveID'] = o.newArchiveID
def sql_to_model_generate(info, o):
    lines = info.split('\n')
    for l in lines:
        str = l.strip()
        words = str.split(' ')
        name = words[0]
        if 'datetime' in words or 'dataTime' in words:
            template = 'res[\'%s\'] = str(%s.%s)' % (name, o, name)
        else:
            template = 'res[\'%s\'] = %s.%s' % (name, o, name)

        print template

# 生产update内容
# companyID = info['companyID'].replace('\'', '\\\'').replace('\"', '\\\"')
def sql_update(info, c):
    lines = info.split('\n')
    for l in lines:
        str = l.strip()
        words = str.split(' ')
        name = words[0]
        stype = words[1]
        # 只有字符串带replace

        # template = "%s.%s : info['%s']," % (c, name, name)
        template = "%s.%s : %s," % (c, name, name)
        print template


# info['companyName'] = companyName
# info['newArchiveID'] = newArchiveID
# info['registerArea'] = registerArea
# info['companyAreaType'] = companyAreaType
# info['certificateID'] = certificateID
def sql_to_generate_info(str):
    lines = str.split('\n')
    for l in lines:
        str = l.strip()
        words = str.split(' ')
        name = words[0]

        template = 'info[\'%s\'] = %s' % (name, name)

        print template

def create_tender(str):
    lines = str.split('\n')
    for l in lines:
        str = l.strip()
        words = str.split(' ')
        name = words[0]

        template = '%s = info[\'%s\'], ' % (name, name)

        print template

if __name__ == '__main__':
    sql = '''userID int comment '用户ID',
    userName nvarchar(100) comment '用户名，昵称',
    info text comment '个人简介，个性签名等',
    portraitPath text comment '头像路径',
    tel nvarchar(20) comment '手机号码',
    email nvarchar(100) comment '电子邮箱',
    gender smallint comment '性别',
    createTime datetime comment '创建时间',
    idCardNum nvarchar(100) comment '身份证号',
    jobPosition nvarchar(100) comment '职位',
    companyName nvarchar(100) comment '公司名称',
    url nvarchar(100) comment '网址',
    addressDescription nvarchar(100) comment '地址',
    longitude nvarchar(20) comment '经度',
    latitude nvarchar(20) comment '维度',
    wechatNum nvarchar(200) comment '微信号',
    QQNum nvarchar(200) comment 'QQ号',
    wechatOfficialAccounts nvarchar(200) comment '微信公众号',
    visitCount int default 0 comment '访问量，人气',
    voteCount int default 0 comment '点赞量',
    favoriteCount int default 0 comment '收藏量',
    backgroundID int comment '背景ID' '''
    sql_to_model_members(sql)
    print '\n'
    sql_to_model_init(sql)
    print '\n'
    sql_to_model_generate(sql, 'o')
    print '\n'
    create_tender(sql)
    print '\n'
    sql_to_model_init_model_param(sql)
    print '\n'
    sql_to_generate_info(sql)
    print '\n'
    sql_to_create_info(sql)
    print '\n'
    sql_update(sql, 'BusinessCard')
