import MySQLdb 
from MySQLdb.cursors import RE_INSERT_VALUES

class GlobalVariables(object):
    def __init__(self, i_var=None):
        self.__i_var_ =i_var
        self.MysqlHost = "localhost"
        self.MysqlUser = "dibankaops"
        self.MysqlPassword = "37f75cac-bcbd-11ea-a5ee-00090ffe0001"
        self.MysqlDataBase = "inversoresnaptrading"
        
        self.__msql= MySQLdb.connect(
            host=self.MysqlHost,
            user=self.MysqlUser,
            password=self.MysqlPassword,
            database=self.MysqlDataBase
        )