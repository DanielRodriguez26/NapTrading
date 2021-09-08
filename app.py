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
from modules.inversor.indicadores import indicadores
from modules.login import loginVerifyModule


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


@app.route('/loginVerify', methods=["GET", "POST"])
def loginVerify():
    try:
        id = request.form['usuario']
        contra = request.form['contrasena']
        render = loginVerifyModule(id,contra)
        return Response(json.dumps({ 'data' : render }), status=200, mimetype='application/json')
    except Exception as error:
        logger.exception(error)

@app.route('/home')
def home():
    try:
        return render_template('index.html')
    except Exception as error:
        logger.exception(error)


@app.route('/indicadores')
def indicadoresUrl():
    try:
        url = indicadores()
        return Response(json.dumps({ 'data' : url }), status=200, mimetype='application/json')
    except Exception as error:
        logger.exception(error)


@app.route('/inversores')
def inversores():
    try:
        return render_template('indicadores.html')
    except Exception as error:
        logger.exception(error)

@app.route('/historicos')
def historicos():
    try:
        return render_template('historicos.html')
    except Exception as error:
        logger.exception(error)


if __name__ == '__main__':
    app.run(port = 2000, debug = True)


