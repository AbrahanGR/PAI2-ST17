import datetime

import psycopg2

def crea_mensaje():
    mensaje = input("Introduce el mensaje: ")
    return mensaje

def registra_mensaje(usuario, mensaje, connection):
    cursor = connection.cursor()
    cursor.execute("INSERT INTO messages (username, msg_content, msg_date) VALUES (%s, %s, %s)", (usuario, mensaje, datetime.datetime.now()))
    '''
    if cursor.fetchone() is None:
        print( "El usuario no existe, creando un nuevo registro")
        cursor.execute("INSERT INTO messages (username, msg_num) VALUES (%s, %s)", (usuario, 1))
    else:
        print("Añadiendo mensaje a la base de datos")
        cursor.execute("UPDATE messages SET msg_num = msg_num + 1 WHERE username = %s", (usuario,))
    '''
    cursor.close()