import MySQLdb 


class GlobalVariables(object):
    def __init__(self, i_var=None):
        self.__i_var_ =i_var
        self.MysqlHost = "localhost"
        self.MysqlUser = "root"
        self.MysqlPassword = "1234"
        self.MysqlDataBase = "inversoresnaptrading"
        
        self.__msql= MySQLdb.connect(
            host=self.MysqlHost,
            user=self.MysqlUser,
            password=self.MysqlPassword,
            database=self.MysqlDataBase
        )