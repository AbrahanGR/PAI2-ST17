# serversocket.py
import socket
import hashing

HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 3030  # Port to listen on (non-privileged ports are > 1023)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print(f"Connected by {addr}")
        while True:
            data = conn.recv(1024)
            if not data:
                break
            conn.sendall(data)


def store_new_user(usuario, contraseña, connection):
    contraseña_hash_salt = hashing.hash_password(contraseña)
    cursor = connection.cursor()
    cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (usuario, contraseña_hash_salt))
    cursor.close()

def login_user(usuario_check, contraseña_check, connection):
    cursor = connection.cursor()
    contraseña_salt = cursor.execute("SELECT password FROM users WHERE username = %s", (usuario_check,))
    return hashing.verify_password(contraseña_check, contraseña_salt)