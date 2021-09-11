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

def indicadoresModule():
    url = render_template('indicadores.html')
    return url

def indicadoresUrlModulo():
    id = session["usuario"]
    objData= collections.OrderedDict()

    cur = mydb.cursor(MySQLdb.cursors.DictCursor)
    cur.execute(" SELECT * FROM usuarios WHERE usuario_id = %s", (id,))
    user = cur.fetchone()
    username = user["username"]
    rol = str(user["rol"])

    if rol == '1':
        cur = mydb.cursor()
        cur.execute(" SELECT * FROM administrativos WHERE usuario_id = %s", (id,))
    else:
        cur = mydb.cursor()
        cur.execute(" SELECT * FROM inversores WHERE usuario_id = %s", (id,))

    data = cur.fetchone()
    nombre = data[3] + ' ' + data[4]
    cur.close()

    objData['nombre'] = nombre
    objData['username'] = username
    objData['url'] = render_template('indicadores.html')

    return objData
