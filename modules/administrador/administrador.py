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



def crearAdministradorModule():
    if request.method == "POST":
        nombre = request.form['nombre']
        apellidos = request.form['apellidos']
        identificacion = request.form['identificacion']
        email = request.form['email']
        telefono = request.form['telefono']

        cur = mydb.cursor()

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
        
        cur.execute('''INSERT INTO usuarios ( username, contrasenia, rol) VALUES (%s,%s,1);''',
                    (username,contrase))
        usuario_id = cur.lastrowid

        cur.execute('''INSERT INTO inversores (usuario_id, identificacion, nombres, apellidos,telefono,email) VALUES (%s,%s,%s,%s,%s,%s);
                    ''',(usuario_id,identificacion, nombre,apellidos,telefono ,email))

        mydb.commit()
        cur.close()
        objData= collections.OrderedDict()
        objData['contra']= contra
        objData['url']= '/home'
        objData['redirect']= True
        objData['username']= username

        return objData





def editarAdministradorModule():
    if request.method == "POST":
        pass


def udateAdministradorModule():
    if request.method == "POST":
        pass


def eliminarAdministradorModule():
    if request.method == "POST":
        pass


def administrarAdministrativosTablaModulo():
    if request.method == "POST":
        pass