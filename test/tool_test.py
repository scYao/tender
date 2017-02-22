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
def sql_to_create_info(info):
    lines = info.split('\n')
    for l in lines:
        str = l.strip()
        words = str.split(' ')
        name = words[0]
        template = "%s = info['%s'].replace(\'\\\'\', \'\\\\\\\'\').replace(\'\\\"\', \'\\\\\\\"\')" % (name, name)
        print template

# create 时, model参数列表
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

def sql_to_model_generate(info, o):
    lines = info.split('\n')
    for l in lines:
        str = l.strip()
        words = str.split(' ')
        name = words[0]

        template = 'res[\'%s\'] = %s.%s' % (name, o, name)

        print template

if __name__ == '__main__':
    sql = '''companyID nvarchar(100) primary key comment '公司ID',
	companyName nvarchar(100) comment '公司名称，单位名称',
	newArchiveID nvarchar(100) comment '新档案号',
	registerArea nvarchar(100) comment '注册地区',
	companyAreaType nvarchar(100) comment '企业地点类别',
	certificateID nvarchar(100) comment '证书编号',
	certificationAuthority nvarchar(100) comment '资质证书, 发证机关',
	legalRepresentative nvarchar(100) comment '法定代表人',
	enterprisePrincipal nvarchar(100) comment '企业负责人',
	technologyDirector nvarchar(100) comment '技术负责人',
	remarks nvarchar(100) comment '备注',
	licenseID nvarchar(100) comment '营业执照, 注册号',
	registeredCapital float comment '注册资本',
	companyType nvarchar(100) comment '公司类型',
	foundingTime date comment '公司成立时间',
	businessTermFrom date comment '营业期限从',
	safetyProductionPermitID nvarchar(100) comment '安全生产许可证ID',
	safePrincipal nvarchar(100) comment '主要负责人',
	range nvarchar(100) comment '许可范围',
	safeAuthority nvarchar(100) comment '安全生产许可证, 发证机关',
	safeFromDate date comment '安全生产许可证, 发证时间',
	safeEndDate date comment '有效期',
	creditBookID nvarchar(100) comment '信用手册ID',
	creditScore1 float comment '信用分，最近半年',
	creditScore2 float comment '信用分，前一个半年',
	creditEndDate date comment '信用手册，有效期',
	creditAuthority nvarchar(100) comment '信用手册, 发证单位',
	creditAddress nvarchar(100) comment '信用手册， 详细地址',
	creditWebSet nvarchar(500) comment '信用手册, 企业网址',
	creditContact nvarchar(100) comment '信用手册, 联系人',
	creditNjAddress nvarchar(100) comment '信用手册, 驻宁地址',
	creditNjPrincipal nvarchar(100) comment '信用手册, 驻宁负责人',
	creditNjTech nvarchar(100) comment '信用手册, 驻宁技术负责人',
	creditFinancialStaff nvarchar(100) comment '信用手册, 驻宁财务负责人',
	companyBrief text comment '公司简介' '''
    # sql_to_create_info(sql)
    sql_to_model_init_model_param(sql)
    # sql_to_model_members(sql)
    # sql_to_model_init(sql)
    # sql_to_model_generate(sql, 'o')