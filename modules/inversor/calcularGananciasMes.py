import MySQLdb
from werkzeug.utils import secure_filename
import globalvariables as gb

def ConnectDataBase():
    globalvariables = gb.GlobalVariables(True)
    return MySQLdb.connect(
    host=globalvariables.MysqlHost,
    user=globalvariables.MysqlUser,
    password=globalvariables.MysqlPassword,
    database=globalvariables.MysqlDataBase)

def calcularGanancias(usuarioID):
    mydb = ConnectDataBase()
    cur = mydb.cursor()    

    cur.execute(''' SELECT i.porcentaje_ganancias ,c.monto, g.monto
                FROM inversores as i
                inner join capital as c on i.usuario_id = c.usuario_id
                inner join ganancias as g on i.usuario_id = g.usuario_id
                where i.usuario_id = %s; ''', (usuarioID,))
    usuarioData = cur.fetchone()          

    # Se buscan todos los ingresos o retiros de capital del afiliado entre el inicio del Pool y hoy
    cur.execute('''select h.monto, h.tipo_movimiento, TIMESTAMPDIFF(DAY, i.fecha_inicio_pool, fecha) 
                    from historicomovimientos as h
                    inner join inversores as i on i.usuario_id = h.usuario_id
                    where fecha between (i.fecha_inicio_pool) and NOW() and tipo_movimiento in ('IC','RC') and h.usuario_id = %s;''',
                (usuarioID,))
    data = cur.fetchall()

    totalCapital = usuarioData[1] + usuarioData[2] # Se suman ganancias y capital

    if usuarioData[0]:
        porcentajeGanancias = usuarioData[0]/100 #Se convierte en % el valor de BD

    #Si no existe un porcentaje definido en la bd se asigna uno dependiendo del total del capital
    else:
        if totalCapital < 10000:
            porcentajeGanancias = 10/100

        elif totalCapital >= 10000 and totalCapital < 30000:
            porcentajeGanancias = 12/100

        elif totalCapital >= 30000 and totalCapital < 50000:
            porcentajeGanancias = 13/100

        elif totalCapital >= 50000:
            porcentajeGanancias = 14/100        

    gananciasMes = totalCapital * porcentajeGanancias # Se sacan las ganancias mes sin tener en cuenta retiros

    #Se calcula las ganancias teniendo en cuentas retiros (RC) o ingresos (IC)
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

    nuevoMontoGanancias = gananciasMes + usuarioData[2] 

    return nuevoMontoGanancias