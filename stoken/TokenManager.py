# coding=utf8
#标准库导入
import sys

from tool.config import ErrorInfo

reload(sys)
sys.setdefaultencoding('utf-8')
sys.path.append('..')
from  datetime import datetime
from tool.Util import Util
from models.flask_app import db
from models.Token import Token
from tool.globals import VALID_PERIOD

class TokenManager(Util):
    def __init__(self):
        pass

    def createToken(self, userID):
        createTime = datetime.now()
        tokenID = self.generateID(userID + str(createTime))
        try:
            db.session.query(Token).filter(
                Token.userID == userID
            ).delete(synchronize_session=False)
            token = Token(tokenID, userID, createTime, VALID_PERIOD)
            db.session.add(token)
            db.session.commit()
        except Exception as e:
            print e
            errorInfo = ErrorInfo['TENDER_02']
            errorInfo['detail'] = str(e)
            db.session.rollback()
            return (False, errorInfo)
        return tokenID

if __name__ == '__main__':
    pass