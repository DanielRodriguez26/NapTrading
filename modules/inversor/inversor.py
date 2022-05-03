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
        buscador = ''
        desde = int(request.values.get('start'))

        mydb = ConnectDataBase()
        cur = mydb.cursor()
        cur.execute('''CALL SP_CONSULTAR_INVERSORES(%s,%s);''', (desde,buscador,))
        data = cur.fetchall()
        cur.close()
        mydb.close()
        dataColl = []
        if data:
            recordsTotal = data[0][6]
            dataColl.append(recordsTotal)
            for row in data:
                objData = collections.OrderedDict()
                objData['usuario_id'] = row[0]
                objData['nombre'] = row[1]
                objData['identificacion'] = row[2]
                objData['email'] = row[3]
                objData['telefono'] = row[4]
                objData['pais'] = row[5]
                dataColl.append(objData)

            return dataColl
        else:
            recordsTotal = 0
            dataColl.append(recordsTotal)
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

def editarInversorFormularioModulo():
    if request.method == "POST":
        usuario_id = request.form['usuario']
        mydb = ConnectDataBase()
        cur = mydb.cursor()
        cur.execute('''SELECT DISTINCT iv.identificacion,
                        iv.nombres, iv.apellidos,
                        iv.email,iv.telefono, 
                        iv.pais, iv.fecha_inicio_pool,
                        gn.monto ,
                        iv.porcentaje_ganancias 
                    FROM inversores iv
                    INNER JOIN ganancias gn ON gn.usuario_id = iv.usuario_id
                    AND iv.usuario_id = %s''', (usuario_id,))
        data = cur.fetchall()

        cur.execute(''' SELECT fecha,disponible ,historico_movimientos_id
                        FROM historicomovimientos 
                        WHERE tipo_movimiento ='IC' 
                        AND disponible > 0
                        AND usuario_id = %s''', (usuario_id,))
        capitales = cur.fetchall()


        cur.close()
        mydb.close()

        
        dataColl = []
        dataCapital = []

        if capitales:
            for capital in capitales:
                objCapital = {}
                fecha = str(capital[0])
                fecha = fecha.split(' ')                
                objCapital['fecha'] = fecha[0]
                objCapital['monto'] = capital[1]
                objCapital['historico_id'] = capital[2]
                dataCapital.append(objCapital)
        if data:
            for row in data:
                fecha_inicio_pool = str(row[6])
                fecha_inicio_pool = fecha_inicio_pool.split(' ')
                objData = collections.OrderedDict()
                objData['identificacion'] = row[0]
                objData['nombres'] = row[1]
                objData['apellidos'] = row[2]
                objData['email'] = row[3]
                objData['telefono'] = row[4]
                objData['pais'] = row[5]
                objData['fecha_inicio_pool'] = fecha_inicio_pool[0]
                objData['ganancia'] = int(row[7])
                objData['porcentaje_ganancias'] = row[8]
                objData['usuario_id'] = usuario_id
                objData['capitales'] = dataCapital
                
                

        dataColl.append(objData)
        return dataColl

def actualizarInversorModulo():
    if request.method == "POST":
        nombres = request.form['nombres']
        apellidos = request.form['apellidos']
        identificacion = request.form['identificacion']
        email = request.form['email']
        telefono = request.form['telefono']
        pais = request.form['pais']
        usuario = request.form['usuario']
        porcentaje_ganancias = request.form['porcentaje_ganancias']            
        fecha_inicio_pool = request.form['fecha_inicio_pool']

        if porcentaje_ganancias == '':
            porcentaje_ganancias = None

        mydb = ConnectDataBase()
        cur = mydb.cursor()

        cur.execute(''' UPDATE inversores   
                        SET nombres = %s , apellidos=%s,email=%s, 
                        telefono=%s, pais=%s, identificacion=%s ,
                        fecha_inicio_pool=%s, porcentaje_ganancias=%s
                        WHERE usuario_id = %s''',
                        (nombres,apellidos,email,telefono,pais, identificacion,fecha_inicio_pool,porcentaje_ganancias,usuario))
        mydb.commit()
        cur.close()
        mydb.close()

        objData = collections.OrderedDict()
        objData['url'] = '/home'
        objData['redirect'] = True
        objData['auditNombre'] = nombres
        objData['auditApellido'] = apellidos
        objData['auditIdentificacion'] = identificacion
        objData['auditEmail'] = email
        objData['auditTelefono'] = telefono
        return objData


def actualizarCapitalModulo():
    if request.method == "POST":
        nombres = request.form['nombres']
        apellidos = request.form['apellidos']
        identificacion = request.form['identificacion']
        email = request.form['email']
        telefono = request.form['telefono']
        pais = request.form['pais']
        usuario = request.form['usuario']
        fechas = json.loads(request.form['fechas'])
        capitales = json.loads(request.form['capital'])

        mydb = ConnectDataBase()
        cur = mydb.cursor()


        if fechas is not None:            
            for fecha in fechas:
                fechaArr = fecha[0]
                feccha = fechaArr['fecha']
                cur.execute(''' UPDATE historicomovimientos   
                            SET fecha=%s WHERE usuario_id = %s''',
                            (feccha,fechaArr['historico_id']))

        if capitales is not None:            
            for capital in capitales:
                capitalArr=capital[0]
                cur.execute(''' UPDATE historicomovimientos   
                            SET disponible=%s WHERE usuario_id = %s''',
                            (capitalArr['monto'],capitalArr['historico_id']))
        
        if 'ganancia' in request.form:
            ganancia = request.form['ganancia']
            mydb.commit()
            cur.execute(''' UPDATE ganancias   
                            SET monto=%s WHERE usuario_id = %s''',
                            (ganancia, usuario))


        mydb.commit()
        cur.close()
        mydb.close()

        objData = collections.OrderedDict()
        objData['url'] = '/home'
        objData['redirect'] = True
        objData['auditNombre'] = nombres
        objData['auditApellido'] = apellidos
        objData['auditIdentificacion'] = identificacion
        objData['auditEmail'] = email
        objData['auditTelefono'] = telefono
        return objData