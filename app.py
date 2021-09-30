from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, g, make_response, session, escape, Response, json
from flask_mysqldb import MySQLdb
from werkzeug.utils import secure_filename


import os
import ast
import logging
import datetime

import modules.authentication as authentication
import modules.globalvariables as gb
import modules.customhash as customhash
import modules.audit as audit
import modules.customhash as customhash


# url
from modules.authentication import permisosModules
from modules.inversor.indicadores import indicadoresModule, indicadoresUrlModulo, retiroganaciasModulo, retiroCapitalModulo
from modules.login import loginVerifyModule
from modules.administrador.administrador import crearAdministradorModule, editarAdministradorModule, administrarAdministrativosTablaModulo
from modules.inversor.inversor import crearInversorModule, administrarInversorTablaModulo, agregarCapitalModule
from modules.historicos import historicosTablaModulo, indicadoresHistoricosModulo,descargarExcelHistoricoModulo
from modules.cambiarContrasena import cambiarContrasenaModulo
from modules.administrador.solicitudes import finalizarTicketModulo, finalizarTicketModuloAudit, solicitudesTablaModulo
from modules.administrador.auditoria import auditoriaTablaModule

app = Flask(__name__)

mydb = None
logger = None
loggerAccess = None
globalvariables = None
UPLOAD_FOLDER = None


def Initial():
    global app, mydb, logger
    try:
        # Configuración logger de errores
        logger = logging.getLogger('')
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s: %(message)s')
        handler = logging.FileHandler('naptrading_error.log')
        handler.setLevel(logging.ERROR)
        handler.setFormatter(formatter)
        logger.addHandler(handler)

        globalvariables = gb.GlobalVariables(True)
        mydb = MySQLdb.connect(
            host=globalvariables.MysqlHost,
            user=globalvariables.MysqlUser,
            password=globalvariables.MysqlPassword,
            database=globalvariables.MysqlDataBase)

        app.secret_key = "TmFwVHJhZGluZyBlcyBjcmVhZGEgcG9yIERhbmllbCBIb3lvcyB5IERhbmllbCBSb2RyaWd1ZXouIHkgZnVlIGNyZWFkbyBwYXJhIGxvcyBpbnZlcnNvcmVzIHkgc3VzIGFkbWluaXN0cmFkb3Jlcy4g"

        UPLOAD_FOLDER = os.path.abspath("./static/img/")

        app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
        app.config["FORMATO_PERMITIDO"] = [
            "PNG", "JPG", "JPEG", "PDF", "DOCX", "DOC"]
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
        clearSession()
        return render_template('login.html')
    except Exception as error:
        logger.exception(error)

# ------------------Login-------------


@app.route("/logout", methods=['POST', 'GET'])
def logout():
    try:
        Initial()
        if session:
            if session.get("SessionId"):
                sessionId = session["SessionId"]
                authentication.logout(sessionId)
                clearSession()
        return redirect("/")

    except Exception as error:
        logger.exception(error)


@app.route('/loginVerify', methods=["GET", "POST"])
def loginVerify():
    try:
        render = loginVerifyModule()
        return Response(json.dumps({'data': render}), status=200, mimetype='application/json')
    except Exception as error:
        logger.exception(error)

# -----------------------------------------


@app.route('/home')
def home():
    try:

        return render_template('index.html')

    except Exception as error:
        logger.exception(error)


@app.route('/permisos')
def permisos():
    try:
        if "usuario" in session:
            dataColl = permisosModules()
            return Response(json.dumps({'data': dataColl}), status=200, mimetype='application/json')
        return render_template("403.html")
    except Exception as error:
        logger.exception(error)

# ------------------indicadores------------


@app.route('/indicadores')
def indicadores():
    try:
        if "usuario" in session:
            dataColl = indicadoresModule()
            return Response(json.dumps({'data': dataColl}), status=200, mimetype='application/json')
        return render_template("403.html")
    except Exception as error:
        logger.exception(error)


@app.route('/indicadoresUrl')
def indicadoresUrl():
    try:
        if "usuario" in session:
            dataColl = indicadoresUrlModulo()
            return Response(json.dumps({'data': dataColl}), status=200, mimetype='application/json')
        return render_template("403.html")
    except Exception as error:
        logger.exception(error)


@app.route('/retirarGanancias', methods=["GET", "POST"])
def retiroganacias():
    try:
        if "usuario" in session:
            dataColl = retiroganaciasModulo()
            return Response(json.dumps({'data': dataColl}), status=200, mimetype='application/json')
        return render_template("403.html")
    except Exception as error:
        logger.exception(error)


@app.route('/retirarCapital', methods=["GET", "POST"])
def retirarCapital():
    try:
        if "usuario" in session:
            dataColl = retiroCapitalModulo()
            return Response(json.dumps({'data': dataColl}), status=200, mimetype='application/json')
        return render_template("403.html")
    except Exception as error:
        logger.exception(error)

# ------------------solicitudes-------------------------


@app.route('/solicitudes')
def solicitudes():
    try:
        if "usuario" in session:
            return render_template('solicitudes.html')
        return render_template("403.html")
    except Exception as error:
        logger.exception(error)


@app.route('/solicitudesTabla', methods=["GET", "POST"])
def solicitudesTabla():
    try:
        if "usuario" in session:
            dataColl = solicitudesTablaModulo()
            recordsTotal = 0
            recordsFiltered = 0
            if len(dataColl) > 0:
                recordsTotal = dataColl[0]
                recordsFiltered = dataColl[0]
                dataColl.remove(recordsTotal)
            return Response(json.dumps({'data': dataColl, 'recordsTotal': recordsTotal, 'recordsFiltered': recordsFiltered}), status=200, mimetype='application/json')
        return render_template("403.html")
    except Exception as error:
        logger.exception(error)


@app.route('/finalizarTicket', methods=["GET", "POST"])
def finalizarTicket():
    try:
        if "usuario" in session:
            dataColl = finalizarTicketModulo()
            objAuditData = finalizarTicketModuloAudit()
            print(objAuditData['monto'])
            auditory = audit.Audit(datetime.datetime.now(), str(session['usuario']), 'Ticket finalizado', 'Se dio por finalizado el ticket '+str(objAuditData['historicoMovimientoId'])+' '+str(objAuditData['tipoMovimiento'])+' del inversor ' + str(objAuditData['nombre'])+' de identificacion '+str(
                objAuditData['identificacion'])+' con fecha limite de '+str(objAuditData['fechaLimite'])+' por un monto de ' + str(objAuditData['monto']) + ' a los siguientes datos ' + str(objAuditData['email']) + ' ' + str(objAuditData['metodo_desembolso']), '')
            audit.AddAudit(auditory)

            return Response(json.dumps({'data': dataColl}), status=200, mimetype='application/json')
        return render_template("403.html")
    except Exception as error:
        logger.exception(error)

# ----------------Auditoria-----------------------------


@app.route('/auditoria')
def auditoria():
    try:
        if "usuario" in session:
            return render_template('auditoria.html')
        return render_template("403.html")
    except Exception as error:
        logger.exception(error)


@app.route('/auditoriaTabla', methods=["GET", "POST"])
def auditoriaTabla():
    try:
        if "usuario" in session:
            dataColl = auditoriaTablaModule()
            recordsTotal = dataColl[0]
            recordsFiltered = dataColl[0]
            dataColl.remove(recordsTotal)
            return Response(json.dumps({'data': dataColl, 'recordsTotal': recordsTotal, 'recordsFiltered': recordsFiltered}), status=200, mimetype='application/json')
        return render_template("403.html")
    except Exception as error:
        logger.exception(error)

# -------------------Inversores------------------------


@app.route('/crearInversores')
def crearInversores():
    try:
        if "usuario" in session:
            return render_template('crearInversores.html')
        return render_template("403.html")
    except Exception as error:
        logger.exception(error)


@app.route('/crearInversor', methods=["GET", "POST"])
def crearInversor():
    try:
        if "usuario" in session:
            objData = crearInversorModule()
            auditory = audit.Audit(datetime.datetime.now(), str(session['usuario']), 'Crear Inversor', 'Se creo el inversor con los siguientes datos: Nombre ' + str(objData['auditNombre'])+', Apellidos '+str(
                objData['auditApellidos'])+', email '+str(objData['auditEmail'])+',  identificación: ' + str(objData['auditIdentificacion'])+', capital:' + str(objData['auditCapital']), '')
            audit.AddAudit(auditory)
            return Response(json.dumps({'data': objData}), status=200, mimetype='application/json')
        return render_template("403.html")
    except Exception as error:
        logger.exception(error)


@app.route('/editarInversores', methods=["GET", "POST"])
def editarInversores():
    try:
        if "usuario" in session:
            return render_template('crearInversores.html')
        return render_template("403.html")
    except Exception as error:
        logger.exception(error)


@app.route('/administrarInversores', methods=["GET", "POST"])
def administrarInversores():
    try:
        if "usuario" in session:
            return render_template('administrarInversores.html')
        return render_template("403.html")
    except Exception as error:
        logger.exception(error)


@app.route('/administrarInversoresTabla', methods=["GET", "POST"])
def administrarInversoresTabla():
    try:
        if "usuario" in session:
            dataColl = administrarInversorTablaModulo()
            recordsTotal = dataColl[0]
            recordsFiltered = dataColl[0]
            dataColl.remove(recordsTotal)
            return Response(json.dumps({'data': dataColl, 'recordsTotal': recordsTotal, 'recordsFiltered': recordsFiltered}), status=200, mimetype='application/json')
        return render_template("403.html")
    except Exception as error:
        logger.exception(error)


@app.route('/agregarCapital', methods=["GET", "POST"])
def agregarCapital():
    try:
        if "usuario" in session:
            usuario_id = request.form['usuario']
            capital = request.form['capital']
            dataColl = agregarCapitalModule(usuario_id, capital)
            auditory = audit.Audit(datetime.datetime.now(), str(session['usuario']), 'Crear Inversor', 'Se creo el inversor con los siguientes datos: Nombre ' + str(dataColl['auditNombre'])+', Apellidos '+str(
                dataColl['auditApellido'])+', email '+str(dataColl['auditEmail'])+',  identificación: ' + str(dataColl['auditIdentificacion'])+', capital:' + str(dataColl['auditCapital']), '')
            audit.AddAudit(auditory)
            return Response(json.dumps({'data': dataColl}), status=200, mimetype='application/json')
        return render_template("403.html")
    except Exception as error:
        logger.exception(error)

# -------------------Administradores---------------------


@app.route('/crearAdministrativos')
def crearAdministrativos():
    try:
        if "usuario" in session:
            return render_template('crearAdministrativos.html')
        return render_template("403.html")
    except Exception as error:
        logger.exception(error)


@app.route('/crearAdministrador', methods=["GET", "POST"])
def crearAdministrador():
    try:
        if "usuario" in session:
            objData = crearAdministradorModule()
            auditory = audit.Audit(datetime.datetime.now(), str(session['usuario']), 'Agregar Capital', 'Se agrego un nuevo capitala al inversor con los siguientes datos: Nombre ' + str(
                objData['auditNombre'])+', Apellidos '+str(objData['auditApellido'])+', email '+str(objData['auditEmail'])+',  identificación: ' + str(objData['auditIdentificacion']) + '')
            audit.AddAudit(auditory)
            return Response(json.dumps({'data': objData}), status=200, mimetype='application/json')
        return render_template("403.html")
    except Exception as error:
        logger.exception(error)


@app.route('/editarAdministrador', methods=["GET", "POST"])
def editarAdministrador():
    try:
        if "usuario" in session:
            objData = editarAdministradorModule()
            auditory = audit.Audit(datetime.datetime.now(), str(
                session['usuario']), 'Cambiar contraseña', 'Se cambio la contraseña del usuario ' + str(objData['usuarioAudit']), '')
            audit.AddAudit(auditory)
            return Response(json.dumps({'data': objData}), status=200, mimetype='application/json')
        return render_template("403.html")
    except Exception as error:
        logger.exception(error)


@app.route('/administrarAdministrativos')
def administrarAdministrativos():
    try:
        if "usuario" in session:
            return render_template('administrarAdministrativos.html')
        return render_template("403.html")
    except Exception as error:
        logger.exception(error)


@app.route('/administrarAdministrativosTabla', methods=["GET", "POST"])
def administrarAdministrativosTabla():
    try:
        if "usuario" in session:
            dataColl = administrarAdministrativosTablaModulo()
            return Response(json.dumps({'data': dataColl}), status=200, mimetype='application/json')
        return render_template("403.html")
    except Exception as error:
        logger.exception(error)


# region  -------------------------Historicos--------------------
@app.route('/historicos')
def historicos():
    try:
        if "usuario" in session:
            return render_template('historicos.html')
        return render_template("403.html")
    except Exception as error:
        logger.exception(error)


@app.route('/historicosTabla', methods=["GET", "POST"])
def historicosTabla():
    try:
        if "usuario" in session:
            dataColl = historicosTablaModulo()
            recordsTotal = dataColl[0]
            recordsFiltered = dataColl[0]
            dataColl.remove(recordsTotal)
            return Response(json.dumps({'data': dataColl, 'recordsTotal': recordsTotal, 'recordsFiltered': recordsFiltered}), status=200, mimetype='application/json')
        return render_template("403.html")
    except Exception as error:
        logger.exception(error)


@app.route('/descargarExcelHistorico', methods=["GET", "POST"])
def descargarExcelHistorico():
    try:
        if "usuario" in session:
            dataColl = descargarExcelHistoricoModulo()
            return Response(json.dumps({'data': dataColl}), status=200, mimetype='application/json')
        return render_template("403.html")
    except Exception as error:
        logger.exception(error)

@app.route('/indicadoresHistoricos')
def indicadoresHistoricos():
    try:
        if "usuario" in session:
            dataColl = indicadoresHistoricosModulo()
            return Response(json.dumps({'data': dataColl}), status=200, mimetype='application/json')
        return render_template("403.html")
    except Exception as error:
        logger.exception(error)


@app.route('/cambiarContrasena')
def cambiarContrasena():
    try:
        if "usuario" in session:
            return render_template('cambiarContrasena.html')
        return render_template("403.html")
    except Exception as error:
        logger.exception(error)
# --------------------------------


@app.route('/cambiarContrasenaLogica', methods=["GET", "POST"])
def cambiarContrasenaLogica():
    try:
        if "usuario" in session:
            dataColl = cambiarContrasenaModulo()
            return Response(json.dumps({'data': dataColl}), status=200, mimetype='application/json')
        return render_template("403.html")
    except Exception as error:
        logger.exception(error)


if __name__ == '__main__':
    app.run(port=2000, debug=True)
