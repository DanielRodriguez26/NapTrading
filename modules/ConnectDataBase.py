import modules.globalvariables as gb
import MySQLdb
def ConnectDataBase():
    globalvariables = gb.GlobalVariables(True)
    return MySQLdb.connect(
    host=globalvariables.MysqlHost,
    user=globalvariables.MysqlUser,
    password=globalvariables.MysqlPassword,
    database=globalvariables.MysqlDataBase)
