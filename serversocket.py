# serversocket.py

import socket
import hmac
import hashlib

import psycopg2

import server_login

HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 3030  # Port to listen on (non-privileged ports are > 1023)
CONNECTION = psycopg2.connect(
    host="localhost",
    port=5432,
    database="PAI1-ST17",
    user="server",
    password="server_PAI1-ST17"
)
CONNECTION.autocommit=True
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print(f"Connected by {addr}")
        while True: #Bucle de inicio de sesión
            data = conn.recv(1024).decode()
            if data == "0":
                break
            elif "," in data:
                print(data)
                datos = data.split(',')
                print(f"recibido: {datos[1]}")
                print(f"recibido: {datos[2]}")

                usuario = datos[1]
                contraseña = datos[2]
                data_server = ""
                if datos[0] == "1":
                    if server_login.login_user(usuario, contraseña, CONNECTION):
                        data_server = "Inicio de sesión exitoso"
                        conn.send(data_server.encode())
                        print(data_server)
                        data_server = ""
                        while True: #Bucle de transacciones
                            data = conn.recv(1024).decode()
                            if data == "0":
                                print("Sesión cerrada")
                                break
                            elif "," in data:
                                datos = data.split(',')
                                #"TODO: Implementar transacciones para usuarios"
                            print(data_server)
                            conn.send(data_server.encode())
                    else:
                        data_server = "No se ha podido iniciar sesión"
                else:
                    server_login.store_new_user(usuario, contraseña, CONNECTION)
                    print("Usuario Registrado")
                    data_server = "Usuario registrado correctamente"

            if not data:
                break
            conn.sendall(data_server.encode())
    CONNECTION.close()
    s.close()
    print("Hasta pronto")