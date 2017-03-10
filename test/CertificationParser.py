# coding=utf8
import re
import sys
import hashlib
reload(sys)
sys.setdefaultencoding('utf-8')
import json
from models.flask_app import db
from tool.Util import Util
from models.CertificationGrade1 import CertificationGrade1
from models.CertificationGrade2 import CertificationGrade2
from models.CertificationGrade3 import CertificationGrade3
from models.CertificationGrade4 import CertificationGrade4

class Certification:
    def __init__(self):
        pass

    def isMathc(self, src,pat):
        pattern = re.compile(pat)
        result = re.match(pattern,src)
        if result == None:
            return 0
        else:
            return 1

    def chargeType(self, character):
        type_num = '\s'
        if self.isMathc(character, type_num) == 1:
            return 1

    def getCharNum(self, str):
        count = 0
        for i in range(len(str)):
            if self.chargeType(str[i])==1:
                count = count + 1
        return count

    def sortData(self, data):
       tabList = []
       tab_1_num, tab_2_num, tab_3_num, tab_4_num = 0, 0, 0, 0
       for line in data:
           line = line.replace('\n', '')
           if line != '':
               dic = {}
               count = int(self.getCharNum(line))
               dic['name'] = line.replace('：', '')
               dic['name'] = dic['name'].replace(':', '').strip()
               dic['list'] = []
               if len(str(line).strip()) != 0 and count > 1:
                   if count < 4:
                       tabList.append(dic)
                       tab_1_num = tab_1_num + 1
                   elif count < 6:
                       list2 = tabList[tab_1_num - 1]['list']
                       list2.append(dic)
                   elif count < 8:
                       list3 = tabList[tab_1_num - 1]['list'][tab_2_num - 1]['list']
                       list3.append(dic)
                   elif count < 10:
                       list4 = tabList[tab_1_num - 1]['list'][tab_2_num - 1]['list'][tab_3_num - 1]['list']
                       list4.append(dic['name'])
       return tabList

    def createCertificationGrade(self, jsonInfo):
        info = json.loads(jsonInfo)
        util = Util()
        for item1 in info:
            c1Dic = {}
            c1Dic['gradeID'] = util.generateID(item1['name'])
            c1Dic['gradeName'] = item1['name']
            (status, result) = CertificationGrade1.create(c1Dic)
            if status:
                db.session.commit()
            for item2 in item1['list']:
                query = db.session.query(CertificationGrade1).filter(
                    CertificationGrade1.gradeName == item1['name']
                )
                result = query.first()
                c2Dic = {}
                c2Dic['gradeID'] = util.generateID(item2['name'])
                c2Dic['gradeName'] = item2['name']
                c2Dic['superiorID'] = result.gradeID
                (status, result) = CertificationGrade2.create(c2Dic)
                if status:
                    db.session.commit()
                for item3 in item2['list']:
                    query = db.session.query(CertificationGrade2).filter(
                        CertificationGrade2.gradeName == item2['name']
                    )
                    result = query.first()
                    c3Dic = {}
                    c3Dic['gradeID'] = util.generateID(item3['name'])
                    c3Dic['gradeName'] = item3['name']
                    c3Dic['superiorID'] = result.gradeID
                    (status, result) = CertificationGrade3.create(c3Dic)
                    if status:
                        db.session.commit()
                    for item4 in item3['list']:
                        if item3['list']:
                            query = db.session.query(CertificationGrade3).filter(
                                CertificationGrade3.gradeName == item3['name']
                            )
                            result = query.first()
                            c4Dic = {}
                            c4Dic['gradeID'] = util.generateID(item4)
                            c4Dic['gradeName'] = item4
                            c4Dic['superiorID'] = result.gradeID
                            (status, result) = CertificationGrade4.create(c4Dic)
                            if status:
                                db.session.commit()








if __name__ == '__main__':

    test = Certification()
    data = './certifications'
    data = open(data, 'r')
    sourceData = json.dumps(test.sortData(data=data))
    test.createCertificationGrade(sourceData)
    data.close()

