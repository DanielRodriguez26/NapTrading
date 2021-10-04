import MySQLdb
from werkzeug.utils import secure_filename
import globalvariables as gb
import customhash as customhash
import uuid

def ConnectDataBase():
    globalvariables = gb.GlobalVariables(True)
    return MySQLdb.connect(
    host=globalvariables.MysqlHost,
    user=globalvariables.MysqlUser,
    password=globalvariables.MysqlPassword,
    database=globalvariables.MysqlDataBase)

def crearInversoresPlano():
    mydb = ConnectDataBase()
    cur = mydb.cursor()

    cur.execute('''SELECT usuario_id FROM usuarios where rol=1''')
    dataIn = cur.fetchall()

    for row in dataIn:     
        
        cur.execute('''SELECT identificacion, nombres, apellidos from inversores where usuario_id = %s;''',
                            (row[0],))
        dataInversor = cur.fetchone()

        identificacion = str(dataInversor[0])
        nombre = str(dataInversor[1])
        apellidos = str(dataInversor[2])
        
        username = nombre[0:1] + apellidos[0:6] + identificacion[-3:]
        username = username.replace(" ", "")
        username = username.lower()

        contra = str(uuid.uuid1())
        contra = contra[0:8]
        contrase = customhash.hash(contra)

        cur.execute(''' UPDATE usuarios 
                            SET contrasenia = %s,
                            username = %s
                            WHERE usuario_id = %s;''',
                            (contrase,username, row[0],))

        cur.execute(''' UPDATE usuariosPlain 
                            SET contrasenia = %s,
                            username = %s
                            WHERE usuario_id = %s;''',
                            (contra,username, row[0],))

    mydb.commit()
    cur.close()
    mydb.close()


crearInversoresPlano()
