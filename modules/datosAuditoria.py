from flask import request
import MySQLdb
from werkzeug.utils import secure_filename
import modules.globalvariables as gb
import collections

globalvariables = gb.GlobalVariables(True)
mydb= MySQLdb.connect(
    host=globalvariables.MysqlHost,
    user=globalvariables.MysqlUser,
    password=globalvariables.MysqlPassword,
    database=globalvariables.MysqlDataBase)  

def datosInversorAuditoria(usuario_id):
    if request.method == "POST":
        movimientoID = request.form['movimientoID']
        cur = mydb.cursor()
        cur.execute('''select i.nombres, i.apellidos,i.identificacion,h.email_solicitud, s.descripcion, h.monto,h.fecha_limite_solicitud, h.metodo_desembolso, h.historico_movimientos_id
                        from historicomovimientos as h
                        inner join inversores as i on i.usuario_id = h.usuario_id
                        inner join siglasmovimientos as s on  s.siglas = h.tipo_movimiento
                        where h.historico_movimientos_id=%s; ''',
                        (movimientoID,))
        auditdata = cur.fetchall()        
        auditDataColl = []
        if auditdata:
            for row in auditdata:
                objAuditData= collections.OrderedDict()
                objAuditData['nombre']= row[0] +' '+row[1]
                objAuditData['identificacion']= row[2]
                objAuditData['email']= row[3]  
                objAuditData['tipoMovimiento']  = row[4]
                objAuditData['monto']  = row[5]                         
                objAuditData['fechaLimite']= row[6]
                objAuditData['metodo_desembolso']  = row[7]
                objAuditData['historicoMovimientoId']  = row[8]
                auditDataColl.append(objAuditData)

    return objAuditData
