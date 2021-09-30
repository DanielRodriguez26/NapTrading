from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, g, make_response, session, escape, Response,json
from datetime import date
from datetime import datetime
import MySQLdb
from werkzeug.utils import secure_filename
import modules.authentication as authentication
import modules.globalvariables as gb
import collections
import xlwt
import io


globalvariables = gb.GlobalVariables(True)
mydb= MySQLdb.connect(
    host=globalvariables.MysqlHost,
    user=globalvariables.MysqlUser,
    password=globalvariables.MysqlPassword,
    database=globalvariables.MysqlDataBase)  


def historicosTablaModulo():
    desde= int(request.values.get('start'))
    cur = mydb.cursor()
    cur.execute('''CALL SP_HISTORICOS(%s,1)''',(desde,))
    data = cur.fetchall()

    cur.close()
    dataColl = []
    
    if data:
        recordsTotal =  data[0][8]
        dataColl.append(recordsTotal)
        for row in data:
            objData= collections.OrderedDict()
            objData['nombre']= row[1] 
            objData['identificacion']= row[2]
            objData['telefono']  = row[3]
            objData['capital']= int(row[4])
            objData['ganancias']= int(row[5])
            objData['totalRetiro']= int(row[6])
            objData['totalReinvertido']= row[7]
            dataColl.append(objData)
    return dataColl

def indicadoresHistoricosModulo():

    cur = mydb.cursor()
    cur.execute('''SELECT COUNT(inversor_id) FROM inversores;''')
    inversores = cur.fetchone()
    cur.close()
    
    cur = mydb.cursor()
    cur.execute('''SELECT IFNULL(SUM(monto),0) as invercion , COUNT(1) total FROM historicomovimientos WHERE tipo_movimiento in ('IC')''')
    inversion = cur.fetchall()
    cur.close()

    cur = mydb.cursor()
    cur.execute('''SELECT IFNULL(SUM(monto),0) as invercion , COUNT(1) total FROM historicomovimientos WHERE tipo_movimiento in ('RG')''')
    gananciasRetiradas = cur.fetchone()
    cur.close()

    inversionM=int(inversion[0][0])
    inversionC=inversion[0][1]
    promedioInversion= inversionM / inversionC


    objData= collections.OrderedDict()
    objData['inversores']= inversores
    objData['inversion']= inversionM
    objData['promedioInversion']  = int(promedioInversion)
    objData['gananciasRetiradas']= int(gananciasRetiradas[0])

    return objData


def descargarExcelHistoricoModulo():
    if request.method == "GET":
        cur = mydb.cursor()
        cur.execute('''CALL SP_HISTORICOS(0,0)''',)
        data = cur.fetchall()


        output = io.BytesIO()
        workbook = xlwt.Workbook()
        sh = workbook.add_sheet('Historico')
        
        #Headers
        sh.write(0, 0, 'Nombre')
        sh.write(0, 1, 'Identificacion')
        sh.write(0, 2, 'Telefono')
        sh.write(0, 3, 'Capital')
        sh.write(0, 4, 'Ganancias')
        sh.write(0, 5, 'Total Retiro')
        sh.write(0, 6, 'Total Reinvertido')

        idx = 0

        for row in data:
            sh.write(idx+1, 0, row[1])
            sh.write(idx+1, 1, row[2])
            sh.write(idx+1, 2, int(row[3]))
            sh.write(idx+1, 3, int(row[4]))
            sh.write(idx+1, 4, int(row[5]))
            sh.write(idx+1, 5, int(row[6]))
            sh.write(idx+1, 6, int(row[7]))

            idx += 1
        idXls = str(datetime.now())
        idXls = idXls.split('.')[0]
        idXls =idXls.replace(':','_')
        idXls =idXls.replace('-','_')
        idXls =idXls.replace(' ','_')
        workbook.save("static/temp/Historicos"+ str(idXls) +".xls")

        url = "/static/temp/Historicos"+ str(idXls) +".xls"
        return  url