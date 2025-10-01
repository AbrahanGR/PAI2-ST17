# serversocket.py

import socket
import hmac
import hashlib

HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 3030  # Port to listen on (non-privileged ports are > 1023)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print(f"Connected by {addr}")
        buffer = ''
        while True:
            data = conn.recv(1024)
            buffer += data.decode()
            while "\n" in buffer:
                mensaje, buffer = buffer.split("\n", 1)
                print("Recibido: " + mensaje)
            '''
            if "," in data:
                datos = data.split(',')
                print(f"recibido: {datos[0]}")
                print(f"recibido: {datos[1]}")

                cifrado = datos[0]
                mensaje = datos[1].encode()
                comprobante = hmac.new(b"clave secreta secretisima", mensaje, hashlib.sha256).hexdigest()

                if hmac.compare_digest(cifrado, comprobante):
                    print("El mensaje es AUTENTICO")
                else:
                    print("El mensaje es FALSO")

            '''
            if not data:
                break
            conn.sendall(data.encode())
