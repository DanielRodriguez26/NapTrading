from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, g, make_response, session, escape, Response,json
import MySQLdb
from werkzeug.utils import secure_filename
import modules.customhash as customhash
import modules.authentication as authentication
import modules.globalvariables as gb
import uuid
import collections

globalvariables = gb.GlobalVariables(True)
mydb= MySQLdb.connect(
    host=globalvariables.MysqlHost,
    user=globalvariables.MysqlUser,
    password=globalvariables.MysqlPassword,
    database=globalvariables.MysqlDataBase)  


def solicitudesTablaModulo():
    if request.method == "POST":
        desde= int(request.values.get('start'))

        cur = mydb.cursor()
        cur.execute('''CALL  SP_CONSULTAR_SOLICITUDES(%s);;''',(desde,))
        data = cur.fetchall()        
        dataColl = []
        if data:
            recordsTotal =  data[0][11]
            dataColl.append(recordsTotal)
            for row in data:
                objData= collections.OrderedDict()
                objData['movimiento_id']= row[0]
                objData['nombre']= row[1] +' '+row[2]
                objData['identificacion']= row[3]
                objData['email']= row[4]
                objData['telefono']= row[5]                
                objData['fecha']= row[6]
                objData['tipoMovimiento']  = row[7]
                objData['monto']  = row[8]
                objData['fechaLimite']  = row[9]
                objData['metodo_desembolso']  = row[10]
                dataColl.append(objData)
        cur.close()
    return dataColl


def finalizarTicketModulo():
    if request.method == "POST":

        movimientoID = request.form['movimientoID']
        cur = mydb.cursor()       

        cur.execute(''' UPDATE historicomovimientos 
                        SET estado = 0 
                        WHERE historico_movimientos_id = %s;''',
                        (movimientoID,))
        mydb.commit()
        cur.close()
        dataColl = []
        
        objData= collections.OrderedDict()
        objData['url']= '/home'
        objData['redirect']= True

        dataColl.append(objData)

    return objData

def finalizarTicketModuloAudit():
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
        cur.close()     
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
