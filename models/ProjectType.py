# -*- coding: utf-8 -*-
import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from flask_app import db

class ProjectType(db.Model):

    __tablename__ = 'ProjectType'
    projectTypeID = db.Column(db.Integer, primary_key=True)
    projectTypeName = db.Column(db.String(100))

    def __init__(self, projectTypeID=0, projectTypeName=None):
        self.projectTypeID = projectTypeID
        self.projectTypeName = projectTypeName

    def __repr__(self):
        return self.projectTypeID


    @staticmethod
    def generate(o):
        res = {}
        res['projectTypeID'] = o.projectTypeID
        res['projectTypeName'] = o.projectTypeName
        return res

