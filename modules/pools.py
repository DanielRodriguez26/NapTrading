import MySQLdb
from werkzeug.utils import secure_filename
from modules.ConnectDataBase import ConnectDataBase
import modules.globalvariables as gb

import collections


def finalizarPool():
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
                totalCapital= row[4] + row[5]
                gananciasMes = totalCapital * 0.10

                # Se buscan todos los ingresos o retiros de capital del afiliado entre el inicio del Pool y hoy
                cur.execute('''select h.monto, h.tipo_movimiento, TIMESTAMPDIFF(DAY, i.fecha_inicio_pool, fecha) 
                                from historicomovimientos as h
                                inner join inversores as i on i.usuario_id = h.usuario_id
                                where fecha between (i.fecha_inicio_pool) and NOW() and tipo_movimiento in ('IC','RC') and h.usuario_id = %s;''',
                            (usuarioID,))
                data = cur.fetchall()

                if data:
                    for row2 in data:

                        if row2[1] == 'IC':
                            monto = row2[0]
                            diasCapital = row2[2] #cuantos días no opero el ingreso de capital
                            ingresoCapital=((int(monto)*0.1)/30)*int(diasCapital)

                            gananciasMes = gananciasMes - ingresoCapital

                        
                        if row2[1] == 'RC':
                            monto = row2[0]
                            diasCapital = row2[2]  #cuantos días operó el total capital actual despues del retiro
                            ingresoCapital=((int(monto)*0.1)/30)*int(diasCapital)
                            gananciasMes = gananciasMes + ingresoCapital
            
                nuevoMontoGanancias = gananciasMes + row[5]

                cur.execute(''' UPDATE ganancias 
                        SET monto = %s 
                        WHERE usuario_id = %s;''',
                        (nuevoMontoGanancias,usuarioID))
                
                cur.execute('''INSERT INTO historicomovimientos ( usuario_id, tipo_movimiento, monto) 
                            VALUES (%s,'IG',%s);''',
                            (usuarioID,gananciasMes))

                cur.execute(''' UPDATE inversores 
                            SET ganancias_mes = 1
                            WHERE usuario_id = %s;''',
                            (usuarioID,))

            if row[3] == 1:
                cur.execute(''' UPDATE inversores 
                            SET ganancias_mes = 0,
                            fecha_inicio_pool = NOW()
                            WHERE usuario_id = %s;''',
                            (usuarioID,))
            else:
                if row[6] > 33:
                    cur.execute(''' UPDATE inversores 
                                SET ganancias_mes = 0,
                                fecha_inicio_pool = NOW()
                                WHERE usuario_id = %s;''',
                                (usuarioID,))
            
            mydb.commit()
    cur.close()
    mydb.close()


finalizarPool()
