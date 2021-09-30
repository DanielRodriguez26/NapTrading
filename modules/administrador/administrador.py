from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, g, make_response, session, escape, Response,json
import MySQLdb
from werkzeug.utils import secure_filename
from modules.ConnectDataBase import ConnectDataBase
import modules.customhash as customhash
import modules.authentication as authentication
import modules.globalvariables as gb
import uuid
import collections



def crearAdministradorModule():
    if request.method == "POST":

        nombre = request.form['nombre']
        apellidos = request.form['apellidos']
        identificacion = request.form['identificacion']
        email = request.form['email']
        telefono = request.form['telefono']
        pais = request.form['pais']

        mydb = ConnectDataBase()
        cur = mydb.cursor()
        objData= collections.OrderedDict()

        cur.execute('''SELECT identificacion, pais FROM administrativos''')
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

        cur.execute('''INSERT INTO administrativos (usuario_id, identificacion, nombre, apellido,telefono,email,pais) VALUES (%s,%s,%s,%s,%s,%s,%s);
                    ''',(usuario_id,identificacion, nombre,apellidos,telefono ,email,pais))

        mydb.commit()

        cur.execute('''SELECT rol FROM usuarios WHERE usuario_id = %s;''',(usuario_id,))
        dataRol= cur.fetchone()
        if dataRol[0] == 1:
            cur.execute('''SELECT identificacion,nombres,apellidos,email FROM inversores WHERE usuario_id = %s;''',(usuario_id,))
            auditData= cur.fetchone()

        else:
            cur.execute('''SELECT identificacion,nombre,apellido,email FROM administrativos WHERE usuario_id = %s;''',(usuario_id,))
            auditData= cur.fetchone()

        auditData=str(auditData[0])

        cur.close()
        mydb.close()
        
        objData['contra']= contra
        objData['url']= '/home'
        objData['redirect']= True
        objData['username']= username
        objData['auditNombre']=auditData[1]
        objData['auditApellido']=auditData[2]
        objData['auditIdentificacion']=auditData[0]
        objData['auditEmail']=auditData[3] 

        return objData


def editarAdministradorModule():
    if request.method == "POST":
        usuario = request.form['usuario']
        contra = str(uuid.uuid1())
        contra = contra[0:5]
        contrase = customhash.hash(contra)

        mydb = ConnectDataBase()
        cur = mydb.cursor()

        cur.execute('''SELECT username FROM usuarios WHERE usuario_id = %s;''',(usuario,))
        data = cur.fetchall()
        username = data[0][0]

        #Se reinician los intentos y el bloqueo-------
        cur.execute(''' UPDATE usuarios 
                        SET contrasenia = %s 
                        WHERE usuario_id = %s;''',
                    (contrase,usuario))  
        cur.execute(''' UPDATE usuarios 
                            SET bloqueo_intentos = 0,
                            usuario_bloqueado= 0
                            WHERE usuario_id = %s;''',
                        (usuario,))
        mydb.commit() 

        #-------Información Auditoria-----------------
        
        cur.execute('''SELECT rol FROM usuarios WHERE usuario_id = %s;''',(usuario,))
        dataRol= cur.fetchone()
        if dataRol[0] == 1:
            cur.execute('''SELECT identificacion FROM inversores WHERE usuario_id = %s;''',(usuario,))
            auditData= cur.fetchone()

        else:
            cur.execute('''SELECT identificacion FROM administrativos WHERE usuario_id = %s;''',(usuario,))
            auditData= cur.fetchone()

        cur.close()
        mydb.close()
        usuarioAudit =auditData[0]
        objData= collections.OrderedDict()
        objData['contra']= contra
        objData['url']= '/home'
        objData['redirect']= True
        objData['username']= username
        objData['usuarioAudit']= usuarioAudit

        return objData


def administrarAdministrativosTablaModulo():
    if request.method == "POST":

        mydb = ConnectDataBase()
        cur = mydb.cursor()
        cur.execute('''SELECT * FROM administrativos''')
        data = cur.fetchall()
        cur.close()
        mydb.close()

        dataColl = []
        if data:
            for row in data:
                objData= collections.OrderedDict()
                objData['usuario_id']= row[1]
                objData['nombre']= row[3] +' '+row[4]
                objData['identificacion']= row[2]
                objData['email']= row[6]
                objData['telefono']  = row[5]
                objData['pais']  = row[7]
                dataColl.append(objData)
    return dataColl