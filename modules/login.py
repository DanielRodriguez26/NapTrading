from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, g, make_response, session, escape, Response,json
from flask_mysqldb import MySQL
from werkzeug.utils import secure_filename

def loginModule():
    return render_template('login.html')
