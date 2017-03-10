#coding:utf-8
import jieba
from pypinyin import lazy_pinyin

from flask_app import app, db
import flask_whooshalchemy as whooshalchemy
class BidSearchKey(db.Model):
    __tablename__ = 'BidSearchKey'
    __searchable__ = ['searchKey']

    joinID = db.Column(db.String(100), primary_key=True)
    biddingID = db.Column(db.String(100))
    searchKey = db.Column(db.Text)
    createTime = db.Column(db.DateTime)

    def __init__(self, joinID=None, biddingID=None,
               searchKey=None, createTime=None):
        self.joinID = joinID
        self.biddingID = biddingID
        self.searchKey = searchKey
        self.createTime = createTime

    def __repr__(self):
        return self.joinID

    @staticmethod
    def createSearchInfo(info):
        title = info['title']
        biddingID = info['biddingID']
        createTime = info['publicDate']
        biddingNum = info['biddingNum']
        joinID = info['joinID']
        # 添加搜索记录
        searchInfo = title +  ',' + biddingNum
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
        bidSearchKey = BidSearchKey(
            joinID=joinID, biddingID=biddingID,
            searchKey=searchInfo, createTime=createTime)
        db.session.add(bidSearchKey)
        return (True, None)


    @staticmethod
    def delete(bidInfo):
        biddingID = bidInfo['biddingID']
        db.session.query(BidSearchKey).filter(
            BidSearchKey.biddingID == biddingID).delete(
            synchronize_session = False
        )
        return (True, None)



# db.create_all()
whooshalchemy.whoosh_index(app, BidSearchKey)