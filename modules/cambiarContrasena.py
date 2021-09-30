from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, g, make_response, session, escape, Response,json
import MySQLdb
from werkzeug.utils import secure_filename
from modules.ConnectDataBase import ConnectDataBase
import modules.customhash as customhash
import modules.authentication as authentication
import modules.globalvariables as gb
import uuid
import collections




def cambiarContrasenaModulo():
    if request.method == "POST":
        contrasena = request.form['contrasena']
        nuevaContrasena = request.form['nuevaContrasena']
        confirmarContrasena = request.form['confirmarContrasena']
        usuario = session['usuario']

        nuevaContrasena = customhash.hash(nuevaContrasena)
        contrasenaForm = customhash.hash(contrasena)
        mydb = ConnectDataBase()
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
            mydb.close()
            return objData

        else:
            mydb.close()
            objData= collections.OrderedDict()
            objData['redirect']= False

            return objData

        
