import MySQLdb
from werkzeug.utils import secure_filename
import globalvariables as gb
from inversor.calcularGananciasMes import calcularGanancias
import logging

def ConnectDataBase():
    globalvariables = gb.GlobalVariables(True)
    return MySQLdb.connect(
    host=globalvariables.MysqlHost,
    user=globalvariables.MysqlUser,
    password=globalvariables.MysqlPassword,
    database=globalvariables.MysqlDataBase)

def finalizarPool():

    #Log de errores
    __loggerAudit = logging.getLogger('NapPools')
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s: %(message)s')
    handler = logging.FileHandler('Nap_error_Pools.log')
    handler.setLevel(logging.ERROR)
    handler.setFormatter(formatter)
    __loggerAudit.addHandler(handler)

    try:
        mydb = ConnectDataBase()
        cur = mydb.cursor()
        cur.execute(''' SELECT i.usuario_id, i.identificacion, i.fecha_inicio_pool, i.reinvertir_ganancias,
                    c.monto, g.monto, TIMESTAMPDIFF(DAY, fecha_inicio_pool, NOW()), ganancias_mes
                    FROM inversores as i
                    inner join capital as c on i.usuario_id = c.usuario_id
                    inner join ganancias as g on i.usuario_id = g.usuario_id; ''')
        usuariosData = cur.fetchall()   
        
        for row in usuariosData:
            usuarioID = row[0]
            #Se valida si ya han pasado 30 días del Pool
            if row[6] >= 30:
                
                #Se valida si aun no se le ha hecho la inserción a ganancias
                if row[7] == 0:                
                    nuevoMontoGanancias=calcularGanancias(usuarioID)

                    cur.execute(''' UPDATE ganancias 
                            SET monto = %s 
                            WHERE usuario_id = %s;''',
                            (nuevoMontoGanancias,usuarioID))
                    
                    cur.execute('''INSERT INTO historicomovimientos ( usuario_id, tipo_movimiento, monto) 
                                VALUES (%s,'IG',%s);''',
                                (usuarioID,nuevoMontoGanancias))

                    cur.execute(''' UPDATE inversores 
                                SET ganancias_mes = 1
                                WHERE usuario_id = %s;''',
                                (usuarioID,))
                                
                    descripcionAuditoria = ' Se han agregado ' + str(nuevoMontoGanancias) + ' a las ganancias del inversor'

                    cur.execute(''' INSERT INTO auditorias 
                        (usuario_id, fecha, accion,
                        descripcion, usuario_ip) 
                        VALUES (%s, NOW(), 'Ingreso Ganancia Mensual', %s, NULL);''',
                        (usuarioID, descripcionAuditoria ))

                if row[3] == 1:
                    cur.execute(''' UPDATE inversores 
                                SET ganancias_mes = 0,
                                fecha_inicio_pool = NOW(),
                                retirar_capital = 3
                                WHERE usuario_id = %s;''',
                                (usuarioID,))
                else:
                    if row[6] > 32:
                        cur.execute(''' UPDATE inversores 
                                    SET ganancias_mes = 0,
                                    fecha_inicio_pool = NOW(),
                                    retirar_capital = 3
                                    WHERE usuario_id = %s;''',
                                    (usuarioID,))
                
                mydb.commit()

        cur.close()
        mydb.close()

    except Exception as error:
            __loggerAudit.exception(error)        
    __loggerAudit.removeHandler(handler)

finalizarPool()
