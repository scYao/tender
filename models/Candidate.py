# -*- coding: utf-8 -*-
import os
import sys

reload(sys)
sys.setdefaultencoding('utf-8')
from flask_app import db

class Candidate(db.Model):
    __tablename__ = 'Candidate'

    candidateID = db.Column(db.String(100), primary_key=True)
    candidateName = db.Column(db.String(100))
    companyID = db.Column(db.String(100))
    price = db.Column(db.Float)
    ranking = db.Column(db.Integer)
    managerName = db.Column(db.String(100))
    managerID = db.Column(db.String(100))
    biddingID = db.Column(db.String(100), db.ForeignKey('WinBiddingPub.biddingID'))

    def __init__(self, candidateID=None, candidateName=None,
                 companyID=None, price=0, ranking=0,
                 managerName=None, managerID=None, biddingID=None):
        self.candidateID = candidateID
        self.candidateName = candidateName
        self.companyID = companyID
        self.price = price
        self.ranking = ranking
        self.managerName = managerName
        self.managerID = managerID
        self.biddingID = biddingID

    @staticmethod
    def generate(c):
        res = {}
        res['candidateID'] = c.candidateID
        res['candidateName'] = c.candidateName
        res['companyID'] = c.companyID
        res['price'] = c.price
        res['ranking'] = c.ranking
        res['managerName'] = c.managerName
        res['managerID'] = c.managerID
        res['biddingID'] = c.biddingID
        return res

    @staticmethod
    def delete(bidInfo):
        biddingID = bidInfo['biddingID']
        db.session.query(Candidate).filter(
            Candidate.biddingID == biddingID).delete(
            synchronize_session=False
        )
        return (True, None)


