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
import modules.login as loginModule


app = Flask(__name__)

mydb = None
logger = None
loggerAccess = None
globalvariables = None
UPLOAD_FOLDER = None


def initial(self):
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
            database=globalvariables.MysqlDatabase)  


        app.secret_key = "RGlCYW5rYTEuMCB3YXMgbWFkZSBmb3IgQ0FTVVIsIGFuZCB3cml0dGVuIGJ5IE1pZ3VlIGFuZCBEYW5pZWwuIEF0IHRoZSBlbmQgb2YgdGhlIHByb2plY3QsIEp1YW4sIEVkd2luLCBIdWdvIGFuZCBBbmRyw6lzIGpvaW5lZCB0aGUgdGVhbS4gTm93IHdlIGFyZSBhIGZpcmVmaWdodGVycyB0ZWFtLg=="

        UPLOAD_FOLDER = os.path.abspath("./static/img/")

        app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
        app.config["FORMATO_PERMITIDO"] = ["PNG", "JPG", "JPEG", "PDF", "DOCX", "DOC"]
        app.config["MAX_IMAGE_FILESIZE"] = 0.5 * 1024 * 1024
    except Exception as error:
        logger.exception(error)

def clearSession():
        # Para mas seguridad, al cargar la landingpage siempre se limpian todas las cookies
    session.clear()

@app.route('/')
def home():
    try:
        return render_template('index.html')

    except Exception as error:
        logger.exception(error)

@app.route('/indicadores')
def indicadores():
    try:
        return render_template('indicadores.html')
    except Exception as error:
        logger.exception(error)

@app.route('/usuarios')
def usuarios():
    try:
        return render_template('indicadores.html')

    except Exception as error:
        logger.exception(error)


if __name__ == '__main__':
    app.run(port = 2000, debug = True)


