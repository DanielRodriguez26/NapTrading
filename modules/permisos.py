from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, g, make_response, session, escape, Response,json
import MySQLdb
from modules.ConnectDataBase import ConnectDataBase
import modules.globalvariables as gb
import collections



def permisosUsuario(parametro):
    usuario_id = session["usuario"]

    mydb = ConnectDataBase()

    cur = mydb.cursor()
    cur.execute('''SELECT rol FROM usuarios where usuario_id = %s''',(usuario_id,))
    data = cur.fetchone()
    cur.close()
    mydb.close()    

    if data[0] != parametro:
        
        return False

    return True

        
    


