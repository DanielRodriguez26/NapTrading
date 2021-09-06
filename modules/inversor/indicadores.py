from flask import Response, json ,render_template
from flask_mysqldb import  MySQLdb


def indicadores():
    url = render_template('indicadores.html')
    return url
