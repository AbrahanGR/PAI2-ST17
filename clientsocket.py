# clientsocket.py

import socket
import hmac
import hashlib
import transacciones

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 3030  # The port used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    #s.sendall(b"Hello, world")
    '''
    clave = b"clave secreta secretisima"
    mensaje = b"comprar pan"
    cifrado = hmac.new(clave, mensaje, hashlib.sha256).hexdigest()+"\n"
    cifrado = cifrado.encode()
    s.sendall(cifrado)
    s.sendall(mensaje)
    '''

    #primero habria que iniciar sesion

    datos_transaccion = transacciones.crea_transaccion()
    emisor = datos_transaccion[0] + '\n'
    receptor = datos_transaccion[1] + '\n'
    cantidad = datos_transaccion[2] + '\n'
    s.sendall(emisor.encode())
    s.sendall(receptor.encode())
    s.sendall(cantidad.encode())

    data = s.recv(1024).decode()
    

print(f"Received {data!r}")
