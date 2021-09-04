import mysql.connector
import datetime
import modules.customhash as customhash
import modules.globalvariables as gb
from flask import request,render_template,url_for, session

globalvariables = gb.GlobalVariables(True)
mydb= mysql.connector.connect(
    host=globalvariables.MyslqlHost,
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