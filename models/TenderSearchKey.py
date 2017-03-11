#coding:utf-8
import jieba
from pypinyin import lazy_pinyin

from flask_app import app, db
import flask_whooshalchemy as whooshalchemy
class TenderSearchKey(db.Model):
    __tablename__ = 'TenderSearchKey'
    __searchable__ = ['searchKey']

    joinID = db.Column(db.String(100), primary_key=True)
    tenderID = db.Column(db.String(100))
    searchKey = db.Column(db.Text)
    createTime = db.Column(db.DateTime)

    def __init__(self, joinID=None, tenderID=None,
               searchKey=None, createTime=None):
        self.joinID = joinID
        self.tenderID = tenderID
        self.searchKey = searchKey
        self.createTime = createTime

    def __repr__(self):
        return self.joinID

    @staticmethod
    def createSearchInfo(info):
        title = info['title']
        tenderID = info['tenderID']
        createTime = info['createTime']
        joinID = info['joinID']
        location = info['location']
        # 添加搜索记录
        searchInfo = title + ',' + location
        # 汉语分词
        fenciList = jieba.cut_for_search(searchInfo)  # 搜索引擎模式
        fenci = " ".join(fenciList)
        # 拼音搜索
        pinyinList = lazy_pinyin(" ".join(jieba.cut_for_search(searchInfo)))
        pinyin = reduce(lambda x, y: x + y, pinyinList)
        pinyinList.append(pinyin)
        pinyinList.append(fenci)
        pinyinList.append(title)
        searchInfo = " ".join(pinyinList)

        tenderSearchKey = TenderSearchKey(
            joinID=joinID, tenderID=tenderID,
            searchKey=searchInfo, createTime=createTime)
        db.session.add(tenderSearchKey)
        return (True, None)

    @staticmethod
    def delete(tenderInfo):
        tenderID = tenderInfo['tenderID']
        db.session.query(TenderSearchKey).filter(
            TenderSearchKey.tenderID == tenderID).delete(
            synchronize_session = False
        )
        return (True, None)



# db.create_all()
whooshalchemy.whoosh_index(app, TenderSearchKey)
