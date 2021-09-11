from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, g, make_response, session, escape, Response,json
import MySQLdb
from werkzeug.utils import secure_filename
import modules.authentication as authentication
import modules.globalvariables as gb
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
        cur = mydb.cursor()


def editarInversorModule():
    if request.method == "POST":
        pass


def udateInversorModule():
    if request.method == "POST":
        pass


def eliminarInversorModule():
    if request.method == "POST":
        pass


def administrarInversorTablaModulo():
    if request.method == "POST":
        pass
