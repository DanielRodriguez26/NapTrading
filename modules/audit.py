import MySQLdb
import logging
import modules.globalvariables as gb
import modules.ipClient as ipClient

class Audit(object):
    def __init__(self, fecha=None, usuario=None, accion=None, descripcion=None, usuario_ip=None):
        self.auditoriaID = None
        self.auditoriaFecha = fecha
        self.auditoriaUsuario = usuario
        self.auditoriaAccion = accion
        self.auditoriaMensaje = descripcion
        self.auditoriaIPAddress = usuario_ip

#Variables globales
__globalvariables = gb.GlobalVariables()
__mysql = None
__loggerAudit = None

def connectDB():
    global __mysql
    __mysql = MySQLdb.connect(
        __globalvariables.MysqlHost, __globalvariables.MysqlUser, __globalvariables.MysqlPassword, __globalvariables.MysqlDataBase)

def AddAudit(audit):
    if print(type(audit)) == print(type(Audit)):
        
        __loggerAudit = logging.getLogger('NapAudit')
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s: %(message)s')
        handler = logging.FileHandler('Nap_error_audit.log')
        handler.setLevel(logging.ERROR)
        handler.setFormatter(formatter)
        __loggerAudit.addHandler(handler)

        try:
            connectDB()
            cur = __mysql.cursor()
            cur.execute('''
                INSERT INTO auditorias 
                    (usuario_id, fecha, accion,
                    descripcion, usuario_ip) 
                VALUES (%s, %s, %s, %s, %s);''',
                (audit.auditoriaUsuario, audit.auditoriaFecha, audit.auditoriaAccion,
                audit.auditoriaMensaje, ipClient.getIPClient()))
            __mysql.commit()
            cur.close()
            __mysql.close()
        except Exception as error:
            __loggerAudit.exception(error)
        
        __loggerAudit.removeHandler(handler)

        
        return True
    else:
        raise Exception("El objeto enviado no es de tipo Audit")

                

