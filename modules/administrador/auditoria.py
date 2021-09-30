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



def auditoriaTablaModule():
    if request.method == "POST":
        desde= int(request.values.get('start'))
        search = request.values.get('search[value]')
        cur = mydb.cursor()
        objData= collections.OrderedDict()

        cur.execute(''' CALL  SP_CONSULTAR_AUDITORIAS(%s,%s);''',(desde,search))
        data = cur.fetchall()
        cur.close()
        dataColl = []
        if data:
            recordsTotal =  data[0][6]
            dataColl.append(recordsTotal)
            for row in data:
                objData= collections.OrderedDict()
                objData['nombre']= row[0] +' '+row[1]
                objData['identificacion']= row[2]
                objData['fecha']= row[3]
                objData['accion']  = row[4]
                objData['descripcion']  = row[5]
                dataColl.append(objData)
        return dataColl