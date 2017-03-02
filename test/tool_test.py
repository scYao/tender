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
        template = "%s = info['%s'].replace(\'\\\'\', \'\\\\\\\'\').replace(\'\\\"\', \'\\\\\\\"\')" % (name, name)
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
    typeDic['text'] = 'Text'
    typeDic['date'] = 'Date'
    typeDic['datetime'] = 'DateTime'
    typeDic['bool'] = 'Boolean'
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
        if pri == 'primary':
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

        template = 'res[\'%s\'] = %s.%s' % (name, o, name)

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

if __name__ == '__main__':
    sql = '''managerID nvarchar(100) primary key comment '项目经理ID',
	managerName nvarchar(100) comment '项目经理姓名',
	gender smallint comment '0 female, 1 male',
	grade nvarchar(100) comment '专业等级',
	positionalTitles nvarchar(100) comment '职称',
	post nvarchar(100) comment '职务',
	safetyAssessment nvarchar(100) comment '安全生产考核证号',
	safeEndDate date comment '有效期',
	safeAuthority nvarchar(100) comment '安全生产考核证号, 发证机关',
	safeFromDate date comment '发证时间' '''
    # sql_to_create_info(sql)
    # sql_to_model_init_model_param(sql)
    sql_to_model_members(sql)
    # sql_to_model_init(sql)
    # sql_to_model_generate(sql, 'o')
    # sql_to_generate_info(sql)