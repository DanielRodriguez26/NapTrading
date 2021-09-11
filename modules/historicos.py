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
    cur = mydb.connection.cursor()
    cur.execute('''CALL SP_CONSULTAR_HISTORICOS(%s)''',(desde,))
    data = cur.fetchall()
    dataColl = []
    if data:
        objData= collections.OrderedDict()
        for row in data:
            objData['nombre']= row[0]
            objData['identificacion']= row[1]
            objData['email']= int(row[2])
            objData['telefono']  = row[3]
            objData['capital']= row[4]
            objData['ganancias']= row[4]
            objData['totalRetiro']= row[4]
            objData['totalReinvertido']= row[4]

        objData['recordsFiltered']= data[0][8]
        objData['recordsTotal'] =  data[0][8]

        dataColl.append(objData)
    return dataColl

def indicadoresHistoricosModulo():
    cur = mydb.connection.cursor()
    cur.execute('''SELECT * FROM historicomovimientos''')
    data = cur.fetchall()
    dataColl = []
    if data:
        objData= collections.OrderedDict()
        for row in data:
            objData['nombre']= row[0]
            objData['identificacion']= row[1]
            objData['email']= int(row[2])
            objData['telefono']  = row[3]
            objData['capital']= row[4]
            objData['ganancias']= row[4]
            objData['totalRetiro']= row[4]
            objData['totalReinvertido']= row[4]

        objData['recordsFiltered']= data[0][8]
        objData['recordsTotal'] =  data[0][8]

        dataColl.append(objData)
    return dataColl
