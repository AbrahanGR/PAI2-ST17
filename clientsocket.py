# clientsocket.py

import socket
import hmac
import hashlib

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 3030  # The port used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    #s.sendall(b"Hello, world")
    clave = b"clave secreta secretisima"
    mensaje = b"comprar pan"
    cifrado = hmac.new(clave, mensaje, hashlib.sha256).hexdigest()+","
    cifrado = cifrado.encode()
    s.sendall(cifrado)
    s.sendall(mensaje)


    data = s.recv(1024).decode()
    

print(f"Received {data!r}")
