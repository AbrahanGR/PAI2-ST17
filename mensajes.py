import psycopg2

def crea_mensaje():
    mensaje = input("Introduce el mensaje: ")
    return mensaje

'''
def comprueba_credenciales(usuario, connection):
    cursor = connection.cursor()
    mensaje = ""
    res = True
    
    
    if cantidad<=0:
        res = False
        mensaje = "Error: ha introducido una cantidad incorrecta"

    
    cursor.execute("SELECT nonce FROM transactions WHERE nonce = %s", (nonce,))
    nonce_repetido = cursor.fetchone()[0]
    if nonce_repetido is not None:
        res = False
        mensaje = "Esta transacción ya se ha hecho"

    cursor.close()
    return res, mensaje
'''
def registra_mensaje(usuario, connection):
    cursor = connection.cursor()
    cursor.execute("SELECT username FROM messages WHERE username = %s", (usuario,))
    if cursor.fetchone() is None:
        print( "El usuario no existe, creando un nuevo registro")
        cursor.execute("INSERT INTO messages (username, msg_num) VALUES (%s, %s)", (usuario, 1))
    else:
        print("Añadiendo mensaje a la base de datos")
        cursor.execute("UPDATE messages SET msg_num = msg_num + 1 WHERE username = %s", (usuario,))
    cursor.close()