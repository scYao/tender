# coding=utf8
import re
import sys
import hashlib
reload(sys)
sys.setdefaultencoding('utf-8')
import json

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
               dic['name'] = line.replace(':', '').strip()
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





if __name__ == '__main__':

    test = Certification()
    data = './certifications'
    data = open(data, 'r')
    print json.dumps(test.sortData(data=data))
    data.close()

