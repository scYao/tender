#coding:utf-8
import jieba
from pypinyin import lazy_pinyin

from flask_app import app, db
import flask_whooshalchemy as whooshalchemy


class MerchandiseSearchKey(db.Model):
    __tablename__ = 'MerchandiseSearchKey'
    __searchable__ = ['searchKey']

    joinID = db.Column(db.String(100), primary_key=True)
    merchandiseID = db.Column(db.String(100))
    # merchandiseID = db.Column(db.String(100), db.ForeignKey('Merchandise.merchandiseID'))
    searchKey = db.Column(db.Text)
    createTime = db.Column(db.DateTime)

    def __init__(self, joinID=None, merchandiseID=None,
               searchKey=None, createTime=None):
        self.joinID = joinID
        self.merchandiseID = merchandiseID
        self.searchKey = searchKey
        self.createTime = createTime

    def __repr__(self):
        return self.joinID

    @staticmethod
    def createSearchInfo(info):
        merchandiseName = info['merchandiseName']
        description = info['description']
        merchandiseID = info['merchandiseID']
        createTime = info['createTime']
        joinID = info['joinID']
        # 添加搜索记录
        searchInfo = merchandiseName + ',' + description
        # 汉语分词
        fenciList = jieba.cut_for_search(searchInfo)  # 搜索引擎模式
        fenci = " ".join(fenciList)
        # 拼音搜索
        pinyinList = lazy_pinyin(" ".join(jieba.cut_for_search(searchInfo)))
        pinyin = reduce(lambda x, y: x + y, pinyinList)
        pinyinList.append(pinyin)
        pinyinList.append(fenci)
        pinyinList.append(merchandiseName)
        searchInfo = " ".join(pinyinList)

        merchandiseSearchKey = MerchandiseSearchKey(
            joinID=joinID, merchandiseID=merchandiseID,
            searchKey=searchInfo, createTime=createTime)
        db.session.add(merchandiseSearchKey)
        return (True, None)

# db.create_all()
whooshalchemy.whoosh_index(app, MerchandiseSearchKey)
