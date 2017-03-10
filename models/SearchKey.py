#coding:utf-8
import jieba
from pypinyin import lazy_pinyin

from flask_app import app, db
import flask_whooshalchemy as whooshalchemy


class SearchKey(db.Model):
    __tablename__ = 'SearchKey'
    __searchable__ = ['searchKey']

    joinID = db.Column(db.String(100), primary_key=True)
    foreignID = db.Column(db.String(100))
    searchKey = db.Column(db.Text)
    createTime = db.Column(db.DateTime)
    tag = db.Column(db.Integer)

    def __init__(self, joinID=None, foreignID=None,
               searchKey=None, createTime=None, tag=0):
        self.joinID = joinID
        self.foreignID = foreignID
        self.searchKey = searchKey
        self.createTime = createTime
        self.tag = tag

    def __repr__(self):
        return self.joinID

    @staticmethod
    def createSearchInfo(info):
        searchName = info['searchName']
        # description = info['description']
        foreignID = info['foreignID']
        createTime = info['createTime']
        joinID = info['joinID']
        # 添加搜索记录
        searchInfo = searchName
        # searchInfo = searchName + ',' + description
        # 汉语分词
        fenciList = jieba.cut_for_search(searchInfo)  # 搜索引擎模式
        fenci = " ".join(fenciList)
        # 拼音搜索
        pinyinList = lazy_pinyin(" ".join(jieba.cut_for_search(searchInfo)))
        pinyin = reduce(lambda x, y: x + y, pinyinList)
        pinyinList.append(pinyin)
        pinyinList.append(fenci)
        pinyinList.append(searchName)
        searchInfo = " ".join(pinyinList)

        searchKey = SearchKey(
            joinID=joinID, foreignID=foreignID,
            searchKey=searchInfo, createTime=createTime)
        db.session.add(searchKey)
        return (True, None)

# db.create_all()
whooshalchemy.whoosh_index(app, SearchKey)
