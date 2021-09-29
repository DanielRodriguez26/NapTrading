from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, g, make_response, session, escape, Response, json
from datetime import datetime, timedelta
import MySQLdb
from werkzeug.utils import secure_filename
import modules.customhash as customhash
import modules.authentication as authentication
import modules.globalvariables as gb
import uuid

import collections

globalvariables = gb.GlobalVariables(True)
mydb = MySQLdb.connect(
    host=globalvariables.MysqlHost,
    user=globalvariables.MysqlUser,
    password=globalvariables.MysqlPassword,
    database=globalvariables.MysqlDataBase)


def indicadoresModule():
    url = render_template('indicadores.html')
    return url


def indicadoresUrlModulo():
    id = session["usuario"]
    objData = collections.OrderedDict()

    cur = mydb.cursor(MySQLdb.cursors.DictCursor)

    cur.execute('''SELECT monto FROM ganancias where usuario_id =%s''', (id,))
    gananciasAcumuladas = cur.fetchone()
    gananciasAcumuladas = gananciasAcumuladas['monto']

    cur.execute('''SELECT monto FROM capital where usuario_id =%s''', (id,))
    capital = cur.fetchone()
    capital = capital['monto']

    cur.execute("SELECT SUM(monto) as totalInvertido, MIN(fecha) as fecha FROM historicomovimientos WHERE tipo_movimiento in ('IC') AND usuario_id = %s and disponible > 0;", (id,))
    totalInvertidos = cur.fetchone()
    totalInvertido = int(totalInvertidos["totalInvertido"])
    fechaIvertida = totalInvertidos["fecha"]

    cur.execute("SELECT SUM(monto) as TotalRetiros FROM historicomovimientos WHERE tipo_movimiento in ('RG','RGC') AND usuario_id = %s", (id,))
    TotalRetiros = cur.fetchone()
    TotalRetiros = int(TotalRetiros["TotalRetiros"])

    cur.execute(" SELECT username FROM usuarios WHERE usuario_id = %s", (id,))
    user = cur.fetchone()
    username = user["username"]

    cur.execute(" SELECT * FROM inversores WHERE usuario_id = %s", (id,))
    data = cur.fetchone()

    nombre = data['nombres'] + ' ' + data['apellidos']
    cur.close()
    fechaPull = data['fecha_inicio_pool']
    fechaPullinicio = str(fechaPull)
    fechaPullinicio = fechaPullinicio.split(' ')[0]


    fechaPullGanancia = str(fechaPull + timedelta(days=30))

    fechaPullGanancia = fechaPullGanancia.split(' ')[0]

    carry, new_month = divmod(fechaIvertida.month-1+6, 12)
    new_month += 1
    fechaIvertida = str(fechaIvertida.replace(year=fechaIvertida.year+carry, month=new_month))
    fechaIvertida = fechaIvertida.split(' ')[0]



    ganancia = capital*10/100
    totalCapital = capital + gananciasAcumuladas
    totalInvertidoAcumulado = capital - totalCapital - TotalRetiros

    objData['username'] = username
    objData['nombre'] = nombre
    objData['capital'] = capital

    objData['totalInvertido'] = totalInvertido
    objData['totalCapital'] = totalCapital
    objData['ganancias'] = ganancia
    objData['gananciasAcumuladas'] = gananciasAcumuladas
    objData['totalInvertidoAcumulado'] = totalInvertidoAcumulado
    objData['fechaPullinicio'] = fechaPullinicio
    objData['fechaPullGanancia'] = fechaPullGanancia
    objData['fechaIvertida'] = fechaIvertida


    objData['url'] = render_template('indicadores.html')

    return objData


def retiroganaciasModulo():
    id = session["usuario"]
    objData = collections.OrderedDict()
    emailRetiro = request.form['emailRetiro']
    gananciaRetiro = int(request.form['gananciaRetiro'])
    metodoRetiro = request.form['metodoRetiro']

    cur = mydb.cursor()
    cur.execute(
        ''' SELECT monto FROM ganancias  WHERE usuario_id = %s;''', (id,))
    monto = cur.fetchone()
    monto = int(monto[0])

    cur.execute(
        ''' SELECT fecha_inicio_pool FROM inversores  WHERE usuario_id = %s;''', (id,))
    fecha_inicio_pool = cur.fetchone()

    cur.execute(
        '''SELECT TIMESTAMPDIFF(DAY, %s, NOW()) AS dias_transcurridos;''', (fecha_inicio_pool,))
    diasTotal = cur.fetchall()

    diasFaltantes = 30 - diasTotal

    if diasTotal > 30:
        if monto >= gananciaRetiro:
            monto = monto-gananciaRetiro

            cur.execute(
                " UPDATE ganancias  SET monto = %s , fecha = NOW() WHERE usuario_id = %s", (monto, id,))

            cur.execute('''INSERT INTO historicomovimientos 
                            (usuario_id, tipo_movimiento, monto, estado,metodo_desembolso,email_solicitud) 
                            VALUES (%s, 'RG', %s, '1' ,%s,%s)''', (id, gananciaRetiro, metodoRetiro, emailRetiro))
            mydb.commit()
            cur.close()

            objData['mensaje'] = 'Holaaa'
            objData['url'] = '/home'
            objData['redirect'] = True

            return objData
        else:
            objData['mensaje'] = 'La cantidad de retio excede el moto que tiene actualmente'
            objData['redirect'] = False
            cur.close()
            return objData
    else:
        objData['mensaje'] = 'Actualmente no es posible hacer un retido sus ganancias ya que hace falta ' + diasFaltantes+' dias '
        objData['redirect'] = False
        cur.close()
        return objData


def retiroCapitalModulo():
    id = session["usuario"]
    objData = collections.OrderedDict()
    emailRetiro = request.form['emailRetiro']
    gananciaRetiro = int(request.form['gananciaRetiro'])
    metodoRetiro = request.form['metodoRetiro']

    cur = mydb.cursor()
    cur.execute(''' SELECT monto FROM capital  WHERE usuario_id = %s;''', (id,))
    monto = cur.fetchone()
    monto = int(monto[0])

    if monto >= gananciaRetiro:
        cur.execute(''' SELECT fecha, monto, historico_movimientos_id FROM historicomovimientos where tipo_movimiento = 'IC' and usuario_id = %s;''', (id,))
        fechaRetiros = cur.fetchall()
        fechaRetiros = fechaRetiros[0]
        montoXCapital = fechaRetiros[1]
        historico_movimientos_id = fechaRetiros[2]

        for fechaRetiro in fechaRetiros:
            fechaRetiro = str(fechaRetiro)
            cur.execute(
                '''SELECT TIMESTAMPDIFF(DAY, %s, NOW()) AS dias_transcurridos;''', (fechaRetiro,))
            diasTotal = cur.fetchall()

            diasFaltantes = 180 - diasTotal
            if diasTotal > 180:
                if montoXCapital >= gananciaRetiro:

                    monto = monto-gananciaRetiro

                    cur.execute(
                        "UPDATE capital  SET monto = %s , fecha = NOW() WHERE usuario_id = %s", (monto, id,))

                    cur.execute("UPDATE historicomovimientos  SET disponible = %s  WHERE historico_movimientos_id = %s", (
                        monto, historico_movimientos_id,))

                    cur.execute('''INSERT INTO historicomovimientos 
                                    (usuario_id, tipo_movimiento, monto, estado,metodo_desembolso,email_solicitud,fecha,fecha_limite_solicitud) 
                                    VALUES (%s, 'RC', %s, '1' ,%s,%s,NOW(),NOW())''', (id, gananciaRetiro, metodoRetiro, emailRetiro))
                    mydb.commit()
                    cur.close()

                    objData['mensaje'] = 'Holaaa'
                    objData['redirect'] = True

                    return objData
                else:
                    objData['mensaje'] = 'La cantidad de retio excede el moto que tiene actualmente'
                    objData['redirect'] = False
                    cur.close()
                    return objData
            else:
                objData['mensaje'] = 'Actualmente no es posible hacer un retido su capital, ya que hace falta ' +diasFaltantes+' dias '
                objData['redirect'] = False
                cur.close()
                return objData
    else:
        objData['mensaje'] = 'La cantidad de retio excede el moto que tiene actualmente'
        objData['redirect'] = False
        cur.close()
        return objData
