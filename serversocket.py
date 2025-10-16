# serversocket.py

import socket
import ssl

import secrets

import psycopg2

import server_login
import mensajes

HOST = "0.0.0.0"
PORT = 3030  # Port to listen on (non-privileged ports are > 1023)

#Certificado y clave
certfile = 'secrets/certs/server_crt.pem'  # Ruta al archivo del certificado SSL
keyfile = 'secrets/keys/server_key.pem'    # Ruta al archivo de la clave privada


# Crear un socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(1)  # Escuchar una conexión

# Envolver el socket con SSL
ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
ssl_context.load_cert_chain(certfile=certfile, keyfile=keyfile)

ssl_context.minimum_version = ssl.TLSVersion.TLSv1_3 #Seleccionamos la version 1.3 para mayor seguridad
cipher_suites = (
    "TLS_AES_256_GCM_SHA384:"
    "TLS_CHACHA20_POLY1305_SHA256:"
    "TLS_AES_128_GCM_SHA256:"
    "ECDHE-ECDSA-AES256-GCM-SHA384:" #Al menos un suite de TLSv1.2 necesario para que lo acepte, aunque vayamos a usar TLSv1.3
)
ssl_context.set_ciphers(cipher_suites)

CONNECTION = psycopg2.connect(
    host="localhost",
    port=5432,
    database="PAI2-ST17",
    user="server",
    password="server_PAI1-ST17"
)
CONNECTION.autocommit=True
with ssl_context.wrap_socket(server_socket, server_side=True) as s:
#with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    #s.bind((HOST, PORT))
    #s.listen()
    conn, addr = s.accept()
    with conn:
        print(f"Connected by {addr}")
        intentos = 5 #Evitar Bruteforce
        while intentos!=0: #Bucle de inicio de sesión
            #print("esperando inicio de sesion")
            data = conn.recv(1024).decode()

            if data == "0":
                break
            elif "," in data:
                #print(data)
                datos = data.split(',')
                print(f"Inicio de sesión: {datos[1]}")

                usuario = datos[1]
                contraseña = datos[2]
                data_server = ""
                if datos[0] == "1":
                    if server_login.login_user(usuario, contraseña, CONNECTION):
                        data_server = "Inicio de sesión exitoso"
                        conn.send((data_server + "," + usuario).encode())
                        print(data_server)
                        data_server = ""
                        while True: #Bucle de transacciones
                            data = conn.recv(1024).decode()
                            #print(data)
                            if data == "0":
                                print("Sesión cerrada")
                                break
                            elif "," in data:
                                datos = data.split(',', maxsplit=1)
                                mensaje = datos[1]
                                #res, mensaje = mensajes.comprueba_credenciales(receptor, cantidad, CONNECTION, nonce)
                                if mensaje != "":
                                    mensajes.registra_mensaje(usuario, mensaje, CONNECTION)
                                    data_server = "Mensaje enviado y recibido correctamente"
                                else:
                                    data_server = "El mensaje está vacío"
                            print(data_server)
                            conn.send(data_server.encode())
                    else:
                        intentos -= 1
                        if intentos != 0:
                            if intentos == 1:
                                data_server = "Usuario o contraseña incorrectos. Le quedan " + str(intentos) + " intento."
                            else:
                                data_server = "Usuario o contraseña incorrectos. Le quedan " + str(intentos) + " intentos."
                        else:
                            print("El usuario ha sobrepasado los intentos")
                            data_server = "Ha agotado sus intentos"
                        conn.send(data_server.encode())
                elif datos[0] == "2":
                    if server_login.store_new_user(usuario, contraseña, CONNECTION):
                        print("Usuario Registrado")
                        data_server = "Usuario registrado correctamente"
                    else:
                        data_server = "El usuario ya existe"
                    conn.send(data_server.encode())
            if not data:
                break
    CONNECTION.close()
    s.close()