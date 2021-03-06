from flask import request,render_template,url_for
from flask_mysqldb import  MySQLdb
from modules.ConnectDataBase import ConnectDataBase
from flask import session
import datetime
import modules.customhash as customhash
import modules.globalvariables as gb
import collections



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
    mydb = ConnectDataBase()
    cur = mydb.cursor(MySQLdb.cursors.DictCursor)
    cur.execute(" SELECT * FROM usuarios WHERE username = %s", (id,))
    user = cur.fetchone()
    cur.close()

    response= collections.OrderedDict()
    
    if user != None:

        hashedPass = customhash.hash(contra)
        contrasena = user["contrasenia"]
        username = user["username"]
        usuario_id = user["usuario_id"]
        rol = str(user["rol"])
        
        if contrasena == hashedPass and username == id:           
            #Se valida el Rol
            if rol == '2':
                
                cur = mydb.cursor()
                cur.execute(" SELECT * FROM administrativos WHERE usuario_id = %s", (usuario_id,))
                data = cur.fetchone()

            else:
                cur = mydb.cursor()
                cur.execute(" SELECT usuario_bloqueado FROM usuarios WHERE usuario_id = %s", (usuario_id,))
                data = cur.fetchone()

                #Se valida si el inversor está bloqueado
                if data[0] == 1:
                    response['url'] = '/'
                    response['redirect'] = False
                    response['bloqueo'] = True
                    response['text']="El usuario se encuentra bloqueado por intentos fallidos, por favor comuniquese con un adminstrador"
                    mydb.close()
                    return response


                else:
                    cur.execute(''' UPDATE usuarios 
                            SET bloqueo_intentos = 0
                            WHERE usuario_id = %s;''',
                        (usuario_id,))                        
                    mydb.commit()        

                    cur.execute(" SELECT * FROM inversores WHERE usuario_id = %s", (usuario_id,))
                    data = cur.fetchone()
                

            nombre = data[3] + ' ' + data[4]

            cur.close()
            mydb.close()
            session["usuario"] = usuario_id
            response['url'] = '/home'
            response['nombre'] = nombre
            response['redirect'] = True
            return response

        else:
            usuario_id = user["usuario_id"]

            if rol == '1':

                cur = mydb.cursor()
                cur.execute(" SELECT usuario_bloqueado FROM usuarios WHERE usuario_id = %s", (usuario_id,))
                data = cur.fetchone()

                #Se valida si el usuario está bloqueado
                if data[0] == 1:
                    response['url'] = '/'
                    response['redirect'] = False
                    response['bloqueo'] = True
                    response['text']="El usuario se encuentra bloqueado por intentos fallidos, por favor comuniquese con un adminstrador"

                    return response

                
                cur.execute(" SELECT bloqueo_intentos FROM usuarios WHERE usuario_id = %s", (usuario_id,))
                data = cur.fetchone()
                intentos= data[0]

                if intentos < 5:

                    intentos=intentos+1

                    cur.execute(''' UPDATE usuarios 
                            SET bloqueo_intentos = %s
                            WHERE usuario_id = %s;''',
                        (intentos,usuario_id))                        
                    mydb.commit()                    
                
                else:
                    cur.execute(''' UPDATE usuarios 
                            SET usuario_bloqueado = 1
                            WHERE usuario_id = %s;''',
                        (usuario_id,))
                    mydb.commit()
                
            cur.close()
            response['url'] = '/'
            response['redirect'] = False

            return response
    else:
            response['url'] = '/'
            response['redirect'] = False
            return response

def permisosModules():
    id = session["usuario"]
    mydb = ConnectDataBase()
    cur = mydb.cursor(MySQLdb.cursors.DictCursor)
    cur.execute(" SELECT * FROM usuarios WHERE usuario_id = %s", (id,))
    user = cur.fetchone()
    cur.close()
    mydb.close()
    response= collections.OrderedDict()
    response = str(user["rol"])
    return response