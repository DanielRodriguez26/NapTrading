from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, g, make_response, session, escape, Response,json
import MySQLdb
from werkzeug.utils import secure_filename
import modules.customhash as customhash
import modules.authentication as authentication
import modules.globalvariables as gb
import uuid
import collections

globalvariables = gb.GlobalVariables(True)
mydb= MySQLdb.connect(
    host=globalvariables.MysqlHost,
    user=globalvariables.MysqlUser,
    password=globalvariables.MysqlPassword,
    database=globalvariables.MysqlDataBase)  



def crearInversorModule():
    if request.method == "POST":
        nombre = request.form['nombre']
        apellidos = request.form['apellidos']
        identificacion = request.form['identificacion']
        email = request.form['email']
        telefono = request.form['telefono']
        pais = request.form['pais']
        capital = request.form['capital']

        cur = mydb.cursor()
        objData= collections.OrderedDict()

        cur.execute('''SELECT identificacion, pais FROM inversores''')
        dataIn = cur.fetchall()
        for row in dataIn:
            if identificacion == str(row[0] and pais == row[1]):
                objData['redirect']= False
                objData['mensaje']= 'El numero de identificacion ya existe'

                return objData


        username = nombre[0:1] + apellidos + identificacion[-3:]
        username = username.lower()
        cur.execute('''SELECT username FROM usuarios''')
        data = cur.fetchall()
        for row in data:            
            if username == row[0]:
                username = nombre[0:1] + apellidos + identificacion[-4:]
                username = username.lower()

        
        contra = str(uuid.uuid1())
        contra = contra[0:5]
        contrase = customhash.hash(contra)
        
        cur.execute('''INSERT INTO usuarios ( username, contrasenia, rol) VALUES (%s,%s,2);''',
                    (username,contrase))
        usuario_id = cur.lastrowid

        cur.execute('''INSERT INTO inversores (usuario_id, identificacion, nombres, apellidos,telefono,email,pais) VALUES (%s,%s,%s,%s,%s,%s,%s);
                    ''',(usuario_id,identificacion, nombre,apellidos,telefono ,email,pais))

        mydb.commit()
        cur.close()
        agregarCapitalModule(usuario_id,capital)
        
        objData['contra']= contra
        objData['url']= '/home'
        objData['redirect']= True
        objData['username']= username

        return objData


def editarInversorModule():
    if request.method == "POST":
        username = request.form['username']
        contra = str(uuid.uuid1())
        contra = contra[0:5]
        contrase = customhash.hash(contra)

        cur = mydb.cursor()
        objData= collections.OrderedDict()
        cur.execute(''' UPDATE usuarios 
                        SET contrasenia = %s 
                        WHERE usuario_id = %s;''',
                    (contrase,username))
        mydb.commit()
        cur.close()

        objData['contra']= contra
        objData['url']= '/home'
        objData['redirect']= True
        objData['username']= username

        return objData


def administrarInversorTablaModulo():
    if request.method == "POST":
        desde= int(request.values.get('start'))
        cur = mydb.cursor()

        cur.execute('''CALL SP_CONSULTAR_INVERSORES(%s);''',(desde,))
        data = cur.fetchall()
        dataColl = []
        if data:
            recordsTotal =  data[0][7]
            dataColl.append(recordsTotal)
            for row in data:
                objData= collections.OrderedDict()
                objData['usuario_id']= row[0]
                objData['nombre']= row[1] +' '+row[2]
                objData['identificacion']= row[3]
                objData['email']= row[4]
                objData['telefono']  = row[5]
                objData['pais']  = row[6]
                dataColl.append(objData)
        return dataColl


def agregarCapitalModule(usuario_id,capital):
    if request.method == "POST":
        cur = mydb.cursor()
        email =None

        cur.execute(''' SELECT 
                        SUM(h.monto),
                        i.email
                        FROM usuarios u
                        INNER JOIN historicomovimientos h on h.usuario_id = u.usuario_id
                        INNER JOIN inversores i on i.usuario_id = u.usuario_id
                        WHERE u.usuario_id =%s''', (usuario_id,))
        data = cur.fetchone()

        catidadHis= int(data[0])

        capitalSum = int(capital)+catidadHis
        email = data[1]

        cur.execute(''' INSERT INTO historicomovimientos
                        (usuario_id,fecha,
                        tipo_movimiento,
                        monto,estado,
                        fecha_limite_solicitud,
                        email_solicitud) 
                        VALUES(%s,NOW(),'IC',%s,0,NOW(),%s)
                    ''',(usuario_id,capital,email))
        historico_id = cur.lastrowid

        cur.execute(''' INSERT INTO capital
                        (historico_movimiento_id,
                        monto,
                        fecha,
                        disponibilidad) 
                        VALUES(%s,%s,NOW(),%s)''',(historico_id,capital,capitalSum))
        mydb.commit()
        cur.close()
        return True





'''def administrarInversorTablaExcelModulo():
    if request.method == "POST":
        desde= int(request.values.get('start'))
        cur = mydb.cursor()

        cur = mysqlPagaduria.cursor()
        cur.execute(,(desde,))
        data = cur.fetchall()
        cur.close()
        mysqlPagaduria.close()

        output = io.BytesIO()
        workbook = xlwt.Workbook()
        sh = workbook.add_sheet('ProductoRetirados')
        
        #Headers
        sh.write(0, 0, 'Nombre')
        sh.write(0, 1, 'Apellidos')
        sh.write(0, 2, 'Desprendible')
        sh.write(0, 3, 'Fecha de Retiro')
        sh.write(0, 4, 'Nombre funcionario que Retiró')
        sh.write(0, 5, 'Código de Descuento')

        idx = 0

        for row in data:
                sh.write(idx+1, 0, row[0])
                sh.write(idx+1, 1, row[1])
                sh.write(idx+1, 2, row[2])
                sh.write(idx+1, 3, row[3])
                sh.write(idx+1, 4, row[4])
                sh.write(idx+1, 5, row[5])

                idx += 1
        idXls = uuid.uuid1()
        workbook.save("static/temp/DescuentosProductoRetiradosDibanka"+ str(idXls) +".xls")
        
        return Response(json.dumps({'url':"/static/temp/Inversores"+ str(idXls) +".xls"}),  mimetype='application/json')'''