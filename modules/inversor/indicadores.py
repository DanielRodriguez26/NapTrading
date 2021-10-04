from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, g, make_response, session, escape, Response, json
from datetime import datetime, timedelta
from modules.ConnectDataBase import ConnectDataBase
import MySQLdb
from werkzeug.utils import secure_filename
import modules.customhash as customhash
import modules.authentication as authentication
import modules.globalvariables as gb
import uuid

import collections




def indicadoresModule():
    url = render_template('indicadores.html')
    return url


def indicadoresUrlModulo():
    if request.method == "GET":
        id = session["usuario"]
        objData = collections.OrderedDict()

        mydb = ConnectDataBase()
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

        cur.execute("SELECT ifnull(SUM(monto), 0) as TotalRetiros FROM historicomovimientos WHERE tipo_movimiento in ('RG','RC') AND usuario_id = %s", (id,))
        TotalRetiros = cur.fetchone()
        TotalRetiros = int(TotalRetiros["TotalRetiros"])

        cur.execute(" SELECT username FROM usuarios WHERE usuario_id = %s", (id,))
        user = cur.fetchone()
        username = user["username"]

        cur.execute(" SELECT * FROM inversores WHERE usuario_id = %s", (id,))
        data = cur.fetchone()

        nombre = data['nombres'] + ' ' + data['apellidos']
        cur.close()
        mydb.close()
        fechaPull = data['fecha_inicio_pool']
        fechaPullinicio = str(fechaPull)
        fechaPullinicio = fechaPullinicio.split(' ')[0]
        check=data['reinvertir_ganancias']


        fechaPullGanancia = str(fechaPull + timedelta(days=30))

        fechaPullGanancia = fechaPullGanancia.split(' ')[0]

        carry, new_month = divmod(fechaIvertida.month-1+6, 12)
        new_month += 1
        fechaIvertida = str(fechaIvertida.replace(year=fechaIvertida.year+carry, month=new_month))
        fechaIvertida = fechaIvertida.split(' ')[0]



        ganancia = capital*10/100
        totalCapital = capital + gananciasAcumuladas
        totalInvertidoAcumulado =  totalCapital -totalInvertido- TotalRetiros

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
        objData['check'] = check
        


        objData['url'] = render_template('indicadores.html')

        return objData


def retiroganaciasModulo():
    if request.method == "POST":
        id = session["usuario"]
        objData = collections.OrderedDict()
        emailRetiro = request.form['emailRetiro']
        gananciaRetiro = request.form['gananciaRetiro']
        metodoRetiro = request.form['metodoRetiro']
        gananciaRetiro = int(gananciaRetiro)
        mydb = ConnectDataBase()
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
        diasTotal = cur.fetchone()

        diasTotal = diasTotal[0]
        diasFaltantes = 30 - diasTotal

        cur.execute(''' SELECT retirar_capital FROM inversores  WHERE usuario_id = %s;''', (id,))
        retirar_capital = cur.fetchone()
        retirar_capital = retirar_capital[0]
        if retirar_capital != 0:
            retirar_capital-=1
            if diasTotal > 30:
                if monto >= gananciaRetiro:
                    monto = monto-gananciaRetiro
                    
                    fecha=datetime.now()
                    fechaEntrega = str(fecha + timedelta(days=3))


                    cur.execute("UPDATE inversores  SET inversores = %s WHERE usuario_id = %s", (retirar_capital, id,))

                    cur.execute(" UPDATE ganancias  SET monto = %s , fecha = NOW() WHERE usuario_id = %s", (monto, id,))

                    cur.execute('''INSERT INTO historicomovimientos 
                                    (usuario_id, tipo_movimiento, monto, estado,metodo_desembolso,email_solicitud,fecha_limite_solicitud) 
                                    VALUES (%s, 'RG', %s, '1' ,%s,%s,%s)''', (id, gananciaRetiro, metodoRetiro, emailRetiro,fechaEntrega))
                    mydb.commit()
                    cur.close()
                    mydb.close()

                    objData['mensaje'] = 'En 3 dias te daran una respuesta de tu retiro'
                    objData['url'] = '/home'
                    objData['redirect'] = True

                    return objData
                else:
                    
                    objData['mensaje'] = 'La cantidad de retio excede el moto que tiene actualmente'
                    objData['redirect'] = False
                    cur.close()
                    mydb.close()
                    return objData
            else:
                objData['mensaje'] = f'Actualmente no es posible hacer un retido sus ganancias ya que hace falta {diasFaltantes} dias '
                objData['redirect'] = False
                cur.close()
                mydb.close()
                return objData

        else: 

            objData['mensaje'] = 'Ya excediste la cantidad de retiros de este mes'
            objData['redirect'] = False
            cur.close()
            mydb.close()
            return objData



def retiroCapitalModulo():
    if request.method == "POST":
        id = session["usuario"]
        objData = collections.OrderedDict()
        emailRetiro = request.form['emailRetiro']
        gananciaRetiro = request.form['gananciaRetiro']
        metodoRetiro = request.form['metodoRetiro']
        gananciaRetiro =int(gananciaRetiro)
        mydb = ConnectDataBase()
        cur = mydb.cursor()
        
        cur.execute(''' SELECT monto FROM capital  WHERE usuario_id = %s;''', (id,))
        monto = cur.fetchone()

        monto = int(monto[0])

        cur.execute(''' SELECT retirar_capital FROM inversores  WHERE usuario_id = %s;''', (id,))
        retirar_capital = cur.fetchone()
        retirar_capital = retirar_capital[0]
        if retirar_capital != 0:
            retirar_capital-=1
            if monto >= gananciaRetiro:
                cur.execute(''' SELECT fecha, monto, historico_movimientos_id FROM historicomovimientos where tipo_movimiento = 'IC' and usuario_id = %s;''', (id,))
                fechaRetiros = cur.fetchall()
                fechaRetiros = fechaRetiros[0]
                montoXCapital = fechaRetiros[1]
                historico_movimientos_id = fechaRetiros[2]

                for fechaRetiro in fechaRetiros:
                    fechaRetiro = str(fechaRetiro)
                    cur.execute(
                        '''SELECT TIMESTAMPDIFF(DAY,NOW(), %s) AS dias_transcurridos;''', (fechaRetiro,))
                    diasTotal = cur.fetchone()

                    diasFaltantes = 180 - diasTotal[0]
                    if diasTotal[0] > 180:
                        if montoXCapital >= gananciaRetiro:
                            
                            fecha=datetime.now()
                            fechaEntrega= str(fecha + timedelta(days=3))


                            monto = monto-gananciaRetiro
                            cur.execute(
                                "UPDATE inversores  SET inversores = %s WHERE usuario_id = %s", (retirar_capital, id,))

                            cur.execute(
                                "UPDATE capital  SET monto = %s , fecha = NOW() WHERE usuario_id = %s", (monto, id,))

                            cur.execute("UPDATE historicomovimientos  SET disponible = %s  WHERE historico_movimientos_id = %s", (
                                monto, historico_movimientos_id,))

                            cur.execute('''INSERT INTO historicomovimientos 
                                            (usuario_id, tipo_movimiento, monto, estado,metodo_desembolso,email_solicitud,fecha,fecha_limite_solicitud) 
                                            VALUES (%s, 'RC', %s, '1' ,%s,%s,NOW(),%s)''', (id, gananciaRetiro, metodoRetiro, emailRetiro,fechaEntrega))
                            mydb.commit()
                            cur.close()
                            mydb.close()

                            objData['mensaje'] = 'En 3 dias te daran una respuesta de tu retiro'
                            objData['url'] = '/home'
                            objData['redirect'] = True

                            return objData
                        else:
                            mydb.close()
                            objData['mensaje'] = 'La cantidad de retio excede el moto que tiene actualmente'
                            objData['redirect'] = False
                            cur.close()
                            return objData
                    else:
                        diasFaltantes=str(diasFaltantes)
                        objData['mensaje'] = f'Actualmente no es posible hacer un retido su capital, ya que hace falta {diasFaltantes} dias '
                        objData['redirect'] = False
                        cur.close()
                        mydb.close()
                        return objData
            else: 
                
                objData['mensaje'] = 'La cantidad de retio excede el moto que tiene actualmente'
                objData['redirect'] = False
                cur.close()
                mydb.close()
                return objData
        else: 
                mydb.close()
                objData['mensaje'] = 'Ya excediste la cantidad de retiros de este mes'
                objData['redirect'] = False
                cur.close()
                return objData


def reuinvertirGananciasModulo():
    if request.method == "POST":
        
        id = session["usuario"]
        estado = request.form['estado']

        mydb = ConnectDataBase()
        cur = mydb.cursor()

        cur.execute("UPDATE inversores  SET reinvertir_ganancias = %s WHERE usuario_id = %s", (estado, id,))

        mydb.commit()
        cur.close()
        mydb.close()
