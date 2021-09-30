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



def cambiarContrasenaModulo():
    if request.method == "POST":
        contrasena = request.form['contrasena']
        nuevaContrasena = request.form['nuevaContrasena']
        confirmarContrasena = request.form['confirmarContrasena']
        usuario = session['usuario']

        nuevaContrasena = customhash.hash(nuevaContrasena)
        contrasenaForm = customhash.hash(contrasena)
        cur = mydb.cursor()
        cur.execute('''SELECT contrasenia FROM usuarios WHERE usuario_id = %s;''',(usuario,))
        data=cur.fetchone()
        contrasenaBD = data[0]

        if contrasenaForm == str(data[0]):
            cur.execute(''' UPDATE usuarios 
                        SET contrasenia = %s 
                        WHERE usuario_id = %s;''',
                    (nuevaContrasena,usuario))
            mydb.commit()
            cur.close()

            objData= collections.OrderedDict()
            objData['url']= '/home'
            objData['redirect']= True

            #'8de3ea8e9fd1484695fba4e6e8ea9cf7e04994147dbf5a097b6f6ac24f6729687b43b0b76647d14c63c89794790068cbf7da002621392db9974f57ca8436480b'
            #'8de3ea8e9fd1484695fba4e6e8ea9cf7e04994147dbf5a097b6f6ac24f6729687b43b0b76647d14c63c89794790068cbf7da002621392db9974f57ca8436480b'
            return objData

        else:
            objData= collections.OrderedDict()
            objData['redirect']= False

            return objData

        
