from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, g, make_response, session, escape, Response, json
from modules.ConnectDataBase import ConnectDataBase
import MySQLdb
from datetime import datetime, timedelta
from werkzeug.utils import secure_filename
import modules.customhash as customhash
import modules.authentication as authentication
import modules.globalvariables as gb
import uuid
import collections




def crearInversorModule():
    if request.method == "POST":
        nombre = request.form['nombre']
        apellidos = request.form['apellidos']
        identificacion = request.form['identificacion']
        email = request.form['email']
        telefono = request.form['telefono']
        pais = request.form['pais']
        capital = request.form['capital']

        mydb = ConnectDataBase()
        cur = mydb.cursor()
        objData = collections.OrderedDict()

        cur.execute('''SELECT identificacion, pais FROM inversores''')
        dataIn = cur.fetchall()
        for row in dataIn:
            if identificacion == str(row[0]) and pais == row[1]:
                objData['redirect'] = False
                objData['mensaje'] = 'El numero de identificacion ya existe'

                return objData

        username = nombre[0:1] + apellidos + identificacion[-3:]
        username = username.replace(" ", "")
        username = username.lower()
        
        cur.execute('''SELECT username FROM usuarios''')
        data = cur.fetchall()
        for row in data:
            if username == row[0]:
                username = nombre[0:1] + apellidos + identificacion[-4:]
                username = username.replace(" ", "")
                username = username.lower()

        contra = str(uuid.uuid1())
        contra = contra[0:5]
        contrase = customhash.hash(contra)

        cur.execute('''INSERT INTO usuarios ( username, contrasenia, rol) VALUES (%s,%s,1);''',
                    (username, contrase))
        usuario_id = cur.lastrowid

        cur.execute('''INSERT INTO  inversores 
                                    (usuario_id, identificacion, 
                                    nombres, apellidos,telefono,
                                    email,pais,fecha_inicio_pool,
                                    reinvertir_ganancias,retirar_capital) 
                        VALUES (%s,%s,%s,%s,%s,%s,%s,NOW(),0,3);
                    ''', (usuario_id, identificacion, nombre, apellidos, telefono, email, pais))
        mydb.commit()
        cur.close()
        mydb.close()

        agregarCapitalModule(usuario_id,capital)

        objData['contra'] = contra
        objData['url'] = '/home'
        objData['redirect'] = True
        objData['username'] = username
        objData['auditNombre'] = nombre
        objData['auditApellidos'] = apellidos
        objData['auditIdentificacion'] = identificacion
        objData['auditEmail'] = email
        objData['auditTelefono'] = telefono
        objData['auditCapital'] = capital

        return objData


def administrarInversorTablaModulo():
    if request.method == "POST":
        desde = int(request.values.get('start'))
        mydb = ConnectDataBase()
        cur = mydb.cursor()

        cur.execute('''CALL SP_CONSULTAR_INVERSORES(%s);''', (desde,))
        data = cur.fetchall()
        cur.close()
        mydb.close()
        dataColl = []
        if data:
            recordsTotal = data[0][7]
            dataColl.append(recordsTotal)
            for row in data:
                objData = collections.OrderedDict()
                objData['usuario_id'] = row[0]
                objData['nombre'] = row[1] + ' '+row[2]
                objData['identificacion'] = row[3]
                objData['email'] = row[4]
                objData['telefono'] = row[5]
                objData['pais'] = row[6]
                dataColl.append(objData)
        return dataColl


def agregarCapitalModule(usuario_id,capital):
    if request.method == "POST":
        mydb = ConnectDataBase()
        cur = mydb.cursor()
        email = None

        cur.execute(
            ''' SELECT monto FROM capital where usuario_id =%s''', (usuario_id,))
        monto = cur.fetchone()

        cur.execute(''' SELECT
                    i.email
                    FROM usuarios u
                    INNER JOIN inversores i on i.usuario_id = u.usuario_id
                    WHERE u.usuario_id =%s''', (usuario_id,))
        data = cur.fetchone()

        
        email = data[0]
        fecha=datetime.now()
        fechaRetiroCpital = str(fecha + timedelta(days=180))


        cur.execute(''' INSERT INTO historicomovimientos
                        (usuario_id,fecha,
                        tipo_movimiento,
                        monto,estado,
                        fecha_limite_solicitud,
                        email_solicitud,
                        disponible) 
                        VALUES(%s,NOW(),'IC',%s,0,NULL,%s,%s)
                    ''', (usuario_id, capital, email, capital))
        historico_id = cur.lastrowid
        if monto is not None:
            
            capitalSum = int(capital) + monto[0]
            cur.execute(''' UPDATE capital  SET monto = %s , fecha = NOW() WHERE usuario_id = %s''',
                        (capitalSum, usuario_id))
        else:
            capital = int(capital)
            cur.execute(''' INSERT INTO capital(usuario_id,monto,fecha,disponibilidad) VALUES(%s,%s,Now(),null);''',
                        (usuario_id, capital,))

            cur.execute(''' INSERT INTO ganancias(usuario_id,monto,fecha,disponibilidad) VALUES(%s,0,Now(),null);''',
                        (usuario_id,))

        mydb.commit()
        cur.execute(
            '''SELECT identificacion,nombres,apellidos,email FROM inversores WHERE usuario_id = %s;''', (usuario_id,))
        auditData = cur.fetchone()

        cur.close()
        mydb.close()

        objData = collections.OrderedDict()

        objData['redirect'] = True
        objData['url'] = '/home'
        objData['auditNombre'] = auditData[1]
        objData['auditApellido'] = auditData[2]
        objData['auditCapital'] = capital
        objData['auditIdentificacion'] = str(auditData[0])
        objData['auditEmail'] = auditData[3]

        return objData



