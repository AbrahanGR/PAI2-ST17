import psycopg2

def crea_transaccion(emisor):
    #emisor = input("Usuario del emisor: ")
    receptor = input("Usuario al que le quieres hacer la transaccion: ")
    cantidad = input("Cantidad que quieres transferir: ")

    return emisor + "," + receptor + "," + cantidad

def comprueba_credenciales(receptor, cantidad, connection, nonce):
    cursor = connection.cursor()
    mensaje = ""
    res = True

    '''
    cursor.execute("SELECT username FROM users WHERE username = %s", (usuario,))
    usuario_encontrado = cursor.fetchone()[0]
    if usuario_encontrado is None:
        print("El usuario emisor no existe")
        res = False
    '''
    
    cursor.execute("SELECT username FROM users WHERE username = %s", (receptor,))
    #usuario_encontrado = cursor.fetchone()[0]
    if cursor.fetchone() is None:
        mensaje = "El usuario receptor no existe"
        res = False
    
    if cantidad<=0:
        res = False
        mensaje = "Error: ha introducido una cantidad incorrecta"

    '''
    cursor.execute("SELECT nonce FROM transactions WHERE nonce = %s", (nonce,))
    nonce_repetido = cursor.fetchone()[0]
    if nonce_repetido is not None:
        res = False
        mensaje = "Esta transacción ya se ha hecho"
    '''

    cursor.close()
    return res, mensaje

def realiza_transaccion(emisor, receptor, cantidad, connection, nonce):
    cursor = connection.cursor()

    cursor.execute("INSERT INTO transactions (origin, dst, amount, nonce) VALUES (%s, %s, %s, %s)", (emisor, receptor, cantidad, nonce))
    cursor.close()