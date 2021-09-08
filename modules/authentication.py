from flask import request,render_template,url_for, session
from flask_mysqldb import  MySQLdb
import datetime
import modules.customhash as customhash
import modules.globalvariables as gb
import collections


globalvariables = gb.GlobalVariables(True)
mydb= MySQLdb.connect(
    host=globalvariables.MysqlHost,
    user=globalvariables.MysqlUser,
    password=globalvariables.MysqlPassword,
    database=globalvariables.MysqlDataBase)  

class authenticateResponse:
    # URL a la que va a ser redirigido el usuario. Puede ser el home de un usuario especifico en caso de que la autenticación sea exitosa, o al mismo formulario
    # de login en caso contrario
    url = ""
    # Algunos formularios de home de usuario requieren que se les envíe el id
    id = 0
    # Algunos formularios requieren que la URL no sea un render_template, sino un redirect. En estos casos se usa redirect en True
    redirect = False
    #Campo para almacenar dinámicante el mensaje de bloque de la tabla Bloqueos.
    mensaje = ""

    isValid = True
    # Determina si el usuario está siendo usado en otro dispositivo
    secondDevic = 0

def authenticate(id, contra):
    cur = mydb.cursor(MySQLdb.cursors.DictCursor)
    cur.execute(" SELECT * FROM usuarios WHERE username=%s", (id,))
    user = cur.fetchone()
    cur.close()
   
    response= collections.OrderedDict()
    
    if user != None:
        hashedPass = customhash.hash(contra)
        contrasena =user["contrasenia"]
        if contrasena == hashedPass:            
            session["usuario"] = id
            response['url']='/home'
            
            return response
        else:
            response['url']='/'
            response['redirect']=True
            return response
    else:
            response['url']='/'
            return response