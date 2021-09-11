from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, g, make_response, session, escape, Response,json
from flask_mysqldb import MySQLdb 
from werkzeug.utils import secure_filename


import os
import ast
import logging
import datetime

import modules.authentication as authentication
import modules.globalvariables as gb
import modules.customhash as customhash


#url
from modules.inversor.indicadores import indicadoresModule ,indicadoresUrlModulo
from modules.login import loginVerifyModule
from modules.administrador.administrador import crearAdministradorModule,editarAdministradorModule,administrarAdministrativosTablaModulo
from modules.inversor.inversor import crearInversorModule,editarInversorModule,administrarInversorTablaModulo
from modules.historicos import historicosTablaModulo,indicadoresHistoricosModulo



app = Flask(__name__)

mydb = None
logger = None
loggerAccess = None
globalvariables = None
UPLOAD_FOLDER = None


def Initial():
    global app, mydb, logger
    try:
        #Configuración logger de errores
        logger = logging.getLogger('')
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s: %(message)s')
        handler = logging.FileHandler('naptrading_error.log')
        handler.setLevel(logging.ERROR)
        handler.setFormatter(formatter)
        logger.addHandler(handler)

        globalvariables = gb.GlobalVariables(True)
        mydb= MySQLdb.connect(
            host=globalvariables.MysqlHost,
            user=globalvariables.MysqlUser,
            password=globalvariables.MysqlPassword,
            database=globalvariables.MysqlDataBase)

        app.secret_key = "TmFwVHJhZGluZyBlcyBjcmVhZGEgcG9yIERhbmllbCBIb3lvcyB5IERhbmllbCBSb2RyaWd1ZXouIHkgZnVlIGNyZWFkbyBwYXJhIGxvcyBpbnZlcnNvcmVzIHkgc3VzIGFkbWluaXN0cmFkb3Jlcy4g"

        UPLOAD_FOLDER = os.path.abspath("./static/img/")

        app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
        app.config["FORMATO_PERMITIDO"] = ["PNG", "JPG", "JPEG", "PDF", "DOCX", "DOC"]
        app.config["MAX_IMAGE_FILESIZE"] = 0.5 * 1024 * 1024
    except Exception as error:
        logger.exception(error)


Initial()


def clearSession():
    # Para mas seguridad, al cargar la landingpage siempre se limpian todas las cookies
    session.clear()


@app.route('/')
def login():
    try:
        return render_template('login.html')
    except Exception as error:
        logger.exception(error)


@app.route("/logout", methods=['POST','GET'])
def logout():
    try:
        Initial()
        if session:
            if session.get("SessionId"):
                sessionId = session["SessionId"]
                authentication.logout(sessionId)
                self.clearSession()
        return redirect("/")

    except Exception as error:
            logger.exception(error)
@app.route('/loginVerify', methods=["GET", "POST"])
def loginVerify():
    try:
        render = loginVerifyModule()
        return Response(json.dumps({ 'data' : render }), status=200, mimetype='application/json')
    except Exception as error:
        logger.exception(error)


@app.route('/home')
def home():
    try:
        return render_template('index.html')
    except Exception as error:
        logger.exception(error)

 #------------------indicadores------------
@app.route('/indicadores')
def indicadores():
    try:
        url = indicadoresModule()
        return Response(json.dumps({ 'data' : url }), status=200, mimetype='application/json')
    except Exception as error:
        logger.exception(error)

@app.route('/indicadoresUrl')
def indicadoresUrl():
    try:
        objData = indicadoresUrlModulo()
        return Response(json.dumps({ 'data' : objData }), status=200, mimetype='application/json')
    except Exception as error:
        logger.exception(error)

#------------------solicitudes-------------------------
@app.route('/solicitudes')
def solicitudes():
    try:
        return render_template('solicitudes.html')
    except Exception as error:
        logger.exception(error)

#----------------Auditoria-----------------------------
@app.route('/auditoria')
def auditoria():
    try:
        return render_template('auditoria.html')
    except Exception as error:
        logger.exception(error)


# -------------------Inversores------------------------
@app.route('/crearInversores')
def crearInversores():
    try:
        return render_template('crearInversores.html')
    except Exception as error:
        logger.exception(error)

@app.route('/crearInversor', methods=["GET", "POST"])
def crearInversor():
    try:
        objData = crearInversorModule()
        return Response(json.dumps({ 'data' : objData }), status=200, mimetype='application/json')
    except Exception as error:
        logger.exception(error)


@app.route('/editarInversores', methods=["GET", "POST"])
def editarInversores():
    try:
        return render_template('crearInversores.html')
    except Exception as error:
        logger.exception(error)


@app.route('/administrarInversores', methods=["GET", "POST"])
def administrarInversores():
    try:
        return render_template('administrarInversores.html')
    except Exception as error:
        logger.exception(error)

@app.route('/administrarInversoresTabla', methods=["GET", "POST"])
def administrarInversoresTabla():
    try:
        dataColl = administrarInversorTablaModulo()
        return Response(json.dumps({ 'data': dataColl }), status=200, mimetype='application/json')
    except Exception as error:
        logger.exception(error)

# -------------------Administradores---------------------
@app.route('/crearAdministrativos')
def crearAdministrativos():
    try:
        return render_template('crearAdministrativos.html')
    except Exception as error:
        logger.exception(error)

@app.route('/crearAdministrador', methods=["GET", "POST"])
def crearAdministrador():
    try:
        objData = crearAdministradorModule()
        return Response(json.dumps({ 'data' : objData }), status=200, mimetype='application/json')
    except Exception as error:
        logger.exception(error)


@app.route('/editarAdministrador', methods=["GET", "POST"])
def editarAdministrador():
    try:
        objData = editarAdministradorModule()
        return Response(json.dumps({ 'data' : objData }), status=200, mimetype='application/json')
    except Exception as error:
        logger.exception(error)


@app.route('/administrarAdministrativos')
def administrarAdministrativos():
    try:
        return render_template('administrarAdministrativos.html')
    except Exception as error:
        logger.exception(error)


@app.route('/administrarAdministrativosTabla', methods=["GET", "POST"])
def administrarAdministrativosTabla():
    try:
        dataColl = administrarAdministrativosTablaModulo()
        return Response(json.dumps({ 'data': dataColl }), status=200, mimetype='application/json')
    except Exception as error:
        logger.exception(error)



#region  -------------------------Historicos--------------------
@app.route('/historicos')
def historicos():
    try:
        return render_template('historicos.html')
    except Exception as error:
        logger.exception(error)

@app.route('/historicosTabla', methods=["GET", "POST"])
def historicosTabla():
    try:
        dataColl = indicadores()
        Response(json.dumps({ 'data':dataColl}), status=200, mimetype='application/json')
    except Exception as error:
        logger.exception(error)

@app.route('/indicadoresHistoricos')
def indicadoresHistoricos():
    try:
        dataColl = indicadores()
        Response(json.dumps({ 'data':dataColl}), status=200, mimetype='application/json')
    except Exception as error:
        logger.exception(error)

#crearInversores

if __name__ == '__main__':
    app.run(port = 2000, debug = True)


