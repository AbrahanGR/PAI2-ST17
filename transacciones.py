import psycopg2

def crea_transaccion():
    emisor = input("Usuario del emisor: ")
    receptor = input("Usuario al que le quieres hacer la transaccion: ")
    cantidad = input("Cantidad que quieres transferir: ")

    return emisor + "," + receptor + "," + cantidad

def comprueba_credenciales(emisor, receptor, cantidad):
    CONNECTION = psycopg2.connect(
    host="localhost",
    port=5432,
    database="PAI1-ST17",
    user="server",
    password="server_PAI1-ST17"
    )
    CONNECTION.autocommit=True

    cursor = CONNECTION.cursor()

    cursor.execute("SELECT username FROM users WHERE username = %s", (emisor,))
    usuario_encontrado = cursor.fetchone()[0]
    if usuario_encontrado is None:
        print("El usuario emisor no existe")
        res = False
    
    cursor.execute("SELECT username FROM users WHERE username = %s", (receptor,))
    usuario_encontrado = cursor.fetchone()[0]
    if usuario_encontrado is None:
        print("El usuario receptor no existe")
        res = False
    
    if cantidad<=0:
        res = False

    res = True
    cursor.close()
    return res

def realiza_transaccion(emisor, receptor, cantidad):
    CONNECTION = psycopg2.connect(
    host="localhost",
    port=5432,
    database="PAI1-ST17",
    user="server",
    password="server_PAI1-ST17"
    )
    CONNECTION.autocommit=True

    cursor = CONNECTION.cursor()

    cursor.execute("INSERT INTO transactions (origin, dst, amount) VALUES (%s, %s, %s)", (emisor, receptor, cantidad))

    print("Transacción realizada correctamente")
    cursor.close()