#coding:utf-8
import jieba
from pypinyin import lazy_pinyin

from flask_app import app, db
import flask_whooshalchemy as whooshalchemy
class UserInfoSearchKey(db.Model):
    __tablename__ = 'UserInfoSearchKey'
    __searchable__ = ['searchKey']

    joinID = db.Column(db.String(100), primary_key=True)
    userID = db.Column(db.String(100))
    searchKey = db.Column(db.Text)
    createTime = db.Column(db.DateTime)

    def __init__(self, joinID=None, userID=None,
               searchKey=None, createTime=None):
        self.joinID = joinID
        self.userID = userID
        self.searchKey = searchKey
        self.createTime = createTime

    def __repr__(self):
        return self.joinID

    @staticmethod
    def createSearchInfo(info):
        title = info['companyName']
        tel = info['tel']
        jobPosition = info['jobPosition']
        joinID = info['joinID']
        userName = info['userName']
        createTime = info['createTime']
        userID = info['userID']
        # 添加搜索记录
        searchInfo = str(title) + ',' + str(tel) + ',' + str(jobPosition) + ',' + str(userName)
        # 汉语分词
        fenciList = jieba.cut_for_search(searchInfo)  # 搜索引擎模式
        fenci = " ".join(fenciList)
        # 拼音搜索
        pinyinList = lazy_pinyin(" ".join(jieba.cut_for_search(searchInfo)))
        pinyin = reduce(lambda x, y: x + y, pinyinList)
        pinyinList.append(pinyin)
        pinyinList.append(fenci)
        pinyinList.append(str(title))
        searchInfo = " ".join(pinyinList)

        userInfoSearchKey = UserInfoSearchKey(
            joinID=joinID, userID=userID,
            searchKey=searchInfo, createTime=createTime)
        db.session.add(userInfoSearchKey)
        return (True, None)

# db.create_all()
whooshalchemy.whoosh_index(app, UserInfoSearchKey)
