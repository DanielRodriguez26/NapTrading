from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, g, make_response, session, escape, Response,json
from flask_mysqldb import MySQL
from werkzeug.utils import secure_filename
import modules.authentication as authentication

def loginModule():
    return render_template('index.html')

def loginVerifyModule(id, contra):
    authenticateResponse = authentication.authenticate(id, contra)
    return authenticateResponse
