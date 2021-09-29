from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, g, make_response, session, escape, Response,json
import MySQLdb
from werkzeug.utils import secure_filename
import modules.authentication as authentication
import modules.globalvariables as gb
import collections


globalvariables = gb.GlobalVariables(True)
mydb= MySQLdb.connect(
    host=globalvariables.MysqlHost,
    user=globalvariables.MysqlUser,
    password=globalvariables.MysqlPassword,
    database=globalvariables.MysqlDataBase)  


def historicosTablaModulo():
    desde= int(request.values.get('start'))
    cur = mydb.cursor()
    cur.execute('''CALL SP_HISTORICOS(%s,1)''',(desde,))
    data = cur.fetchall()

    cur.close()
    dataColl = []
    
    if data:
        recordsTotal =  data[0][8]
        dataColl.append(recordsTotal)
        for row in data:
            objData= collections.OrderedDict()
            objData['nombre']= row[1] 
            objData['identificacion']= row[2]
            objData['telefono']  = row[3]
            objData['capital']= int(row[4])
            objData['ganancias']= int(row[5])
            objData['totalRetiro']= int(row[6])
            objData['totalReinvertido']= row[7]
            dataColl.append(objData)
    return dataColl

def indicadoresHistoricosModulo():

    cur = mydb.cursor()
    cur.execute('''SELECT COUNT(1) FROM inversores''')
    inversores = cur.fetchone()
    
    cur.execute('''SELECT IFNULL(SUM(monto),0) as invercion , COUNT(1) total FROM historicomovimientos WHERE tipo_movimiento in ('IC')''')
    inversion = cur.fetchall()

    cur.execute('''SELECT IFNULL(SUM(monto),0) as invercion , COUNT(1) total FROM historicomovimientos WHERE tipo_movimiento in ('RG')''')
    gananciasRetiradas = cur.fetchone()
    cur.close()

    inversionM=int(inversion[0][0])
    inversionC=inversion[0][1]
    promedioInversion= inversionM / inversionC


    objData= collections.OrderedDict()
    objData['inversores']= inversores
    objData['inversion']= inversionM
    objData['promedioInversion']  = int(promedioInversion)
    objData['gananciasRetiradas']= int(gananciasRetiradas[0])

    return objData
