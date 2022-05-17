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

        cur.execute("SELECT SUM(h.disponible) as totalInvertido, MIN(h.fecha) as fecha, DATE_ADD(MIN(h.fecha),INTERVAL 180 DAY) as fechaRetiro FROM historicomovimientos as h WHERE tipo_movimiento in ('IC') AND usuario_id = %s and disponible >= 0;", (id,))
        totalInvertidos = cur.fetchone()
        totalInvertido = int(totalInvertidos["totalInvertido"])
        fechaIvertida = str(totalInvertidos["fechaRetiro"])

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


        fechaPullGanancia = str(fechaPull + timedelta(days=31))

        fechaPullGanancia = fechaPullGanancia.split(' ')[0]

        fechaIvertida = fechaIvertida[0:10]



        ganancia = capital*10/100
        totalCapital = capital + gananciasAcumuladas
        totalInvertidoAcumulado =  totalCapital - totalInvertido - TotalRetiros
        if totalInvertidoAcumulado < 0:
            totalInvertidoAcumulado = 0

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
        if diasTotal > 30:
            if monto >= gananciaRetiro:
                monto = monto-gananciaRetiro
                
                fecha=datetime.now()
                fechaEntrega = str(fecha + timedelta(days=3))

                cur.execute(" UPDATE ganancias  SET monto = %s , fecha = NOW() WHERE usuario_id = %s", (monto, id,))

                cur.execute('''INSERT INTO historicomovimientos 
                                (usuario_id, tipo_movimiento, monto, estado,metodo_desembolso,email_solicitud,fecha_limite_solicitud) 
                                VALUES (%s, 'RG', %s, '1' ,%s,%s,%s)''', (id, gananciaRetiro, metodoRetiro, emailRetiro,fechaEntrega))
                mydb.commit()
                cur.close()
                mydb.close()

                objData['mensaje'] = 'En maximo 3 días se dara respuesta a tu retiro'
                objData['url'] = '/home'
                objData['redirect'] = True

                return objData
            else:
                
                objData['mensaje'] = 'La cantidad de retiro excede el monto que tiene actualmente'
                objData['redirect'] = False
                cur.close()
                mydb.close()
                return objData
        else:
            objData['mensaje'] = f'Actualmente no es posible hacer un retiro sus ganancias ya que hace falta {diasFaltantes} días '
            objData['redirect'] = False
            cur.close()
            mydb.close()
            return objData



def retiroCapitalModulo():
    if request.method == "POST":
        id = session["usuario"]
        objData = collections.OrderedDict()
        emailRetiro = request.form['emailRetiro']
        capitalRetiro = request.form['gananciaRetiro']
        metodoRetiro = request.form['metodoRetiro']
        capitalRetiro =int(capitalRetiro)
        mydb = ConnectDataBase()
        cur = mydb.cursor()
        
        cur.execute(''' SELECT monto FROM capital  WHERE usuario_id = %s;''', (id,))
        monto = cur.fetchone()

        monto = int(monto[0])

        cur.execute(''' SELECT retirar_capital FROM inversores  WHERE usuario_id = %s;''', (id,))
        retirar_capital = cur.fetchone()
        retirar_capital = retirar_capital[0]
        if retirar_capital > 0:
            retirar_capital-=1
            #Se valida si la solicitud del inversor es menor al capital que posee
            if monto >= capitalRetiro:
                #Se valida si han pasado 6 meses al menos en un ingreso de Capital para continuar
                cur.execute('''select min(historico_movimientos_id), fecha, TIMESTAMPDIFF(DAY, fecha, NOW()) from historicomovimientos where TIMESTAMPDIFF(DAY, fecha, NOW()) > 180 and tipo_movimiento = 'IC' and disponible > 0 and usuario_id =%s;''', (id,))
                diasFaltantes = cur.fetchone()

                if diasFaltantes[0]:
                    # Se busca en los historicos del inversor cuanto disponible tienen ingresos de capital que superen 180 días
                    cur.execute(''' select sum(disponible) from historicomovimientos where TIMESTAMPDIFF(DAY, fecha, NOW()) > 180 and tipo_movimiento = 'IC' and usuario_id = %s;''', (id,))
                    totalDisponible = cur.fetchone()

                    if totalDisponible[0]> capitalRetiro:

                        cur.execute(''' select historico_movimientos_id, disponible from historicomovimientos where TIMESTAMPDIFF(DAY, fecha, NOW()) > 180 and tipo_movimiento = 'IC' and disponible > 0 and usuario_id =%s;''', (id,))
                        ICmovimientos = cur.fetchall()

                        capitalRetiroDesc = capitalRetiro

                        for ICmovimiento in ICmovimientos:
                            # Se valida en cada iteración que haya capital, cada ciclo va a ir restando y actualizando los disponibles de los historicos hasta que quede en 0 
                            if capitalRetiroDesc > 0:

                                ingresoCapitalID =  ICmovimiento[0]
                                disponibleIC = ICmovimiento[1]

                                if disponibleIC <= capitalRetiroDesc:
                                    capitalRetiroDesc = capitalRetiroDesc - disponibleIC
                                    disponibleIC = 0
                                
                                else:
                                    disponibleIC = disponibleIC - capitalRetiroDesc
                                    capitalRetiroDesc = 0

                                cur.execute("UPDATE historicomovimientos  SET disponible = %s  WHERE historico_movimientos_id = %s", (
                                    disponibleIC, ingresoCapitalID,))
                            else: 
                                break

                        cur.execute("UPDATE inversores  SET retirar_capital = %s WHERE usuario_id = %s", (retirar_capital, id,))
                        monto = monto - capitalRetiro  

                        fecha=datetime.now()
                        fechaEntrega= str(fecha + timedelta(days=3))

                        cur.execute("UPDATE capital  SET monto = %s , fecha = NOW() WHERE usuario_id = %s", (monto, id,))
                        cur.execute('''INSERT INTO historicomovimientos 
                                        (usuario_id, tipo_movimiento, monto, estado,metodo_desembolso,email_solicitud,fecha,fecha_limite_solicitud) 
                                        VALUES (%s, 'RC', %s, '1' ,%s,%s,NOW(),%s)''', (id, capitalRetiro, metodoRetiro, emailRetiro,fechaEntrega))
                        mydb.commit()
                        cur.close()
                        mydb.close()

                        objData['mensaje'] = 'En maximo 3 días se dara respuesta a su retiro'
                        objData['url'] = '/home'
                        objData['redirect'] = True
                        return objData                            
                                
                    else:
                        totalDisponible=str(totalDisponible[0])
                        objData['mensaje'] = 'La cantidad de retiro excede el monto que actualmente puede retirar, el capital debe estar un minimo de 6 meses para poder ser retirado, actualmente puede retirar $'+ totalDisponible
                        objData['redirect'] = False
                        cur.close()
                        mydb.close()
                        return objData
                else:
                    diasFaltantes=str(diasFaltantes)
                    objData['mensaje'] = f'Actualmente no es posible hacer un retiro su capital'
                    objData['redirect'] = False
                    cur.close()
                    mydb.close()
                    return objData
            else: 
                
                objData['mensaje'] = 'La cantidad de retiro excede el monto que tiene actualmente'
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
