# coding=utf8
import base64
import sys
import json
import urllib
import urllib2

from Crypto.Cipher import AES
from tool.tagconfig import RIGHT_TAG_CONTRACT

sys.path.append("..")
import os, random, requests
reload(sys)
sys.setdefaultencoding('utf-8')

from datetime import datetime
import hashlib
from sqlalchemy import and_, text, func, desc
import traceback
from models.flask_app import db
from models.UserInfo import UserInfo
from models.Contract import Contract
from tool.Util import Util
from tool.config import ErrorInfo

class ContractProjectProcessManager(Util):
    def __init__(self):
        pass

    def createContractProjectProces(self, info):
        pass