import hashlib
import os
import random

import psycopg2
from psycopg2 import sql

import hashing
import server_login

#Conexión con el usuario administrador para crear las tablas y darle permiso al usuario servidor
connection = psycopg2.connect(
    host="localhost",
    port=5432,
    database="PAI2-ST17",
    user="admin",
    password="admin_PAI1-ST17"
)

connection.autocommit = True
cursor = connection.cursor()

cursor.execute("DROP TABLE IF EXISTS users")
cursor.execute("CREATE TABLE users (username VARCHAR(255) PRIMARY KEY, password VARCHAR(113))") #contraseña: 64(256 bits/32 bytes) + ":" + salt: 48(192 bits/24 bytes) = 113 caracteres hex

#Introducir usuarios prerregistrados
hash1 = hashing.hash_password("P3p3*sEgUrO*1nd3sc1fr4bl3")
hash2 = hashing.hash_password("PEpA_s3gur4_IndEscIfRAblE")
server_login.store_new_user("pepe", hash1, connection)
server_login.store_new_user("pepa", hash2, connection)

cursor.execute("DROP TABLE IF EXISTS messages")
cursor.execute("CREATE TABLE messages (username VARCHAR(255), msg_content VARCHAR(255), msg_date TIMESTAMP PRIMARY KEY)") #nonce: 32(128 bits/16 bytes)

#Le damos permisos de lectura, escritura y edición de los datos sobre las tablas
cursor.execute(sql.SQL("GRANT SELECT, INSERT, UPDATE ON ALL TABLES IN SCHEMA public TO {};").format(sql.Identifier("server")))

cursor.execute(sql.SQL("GRANT USAGE ON ALL SEQUENCES IN SCHEMA public TO {};").format(sql.Identifier("server")))

cursor.close()
connection.close()

print("Tablas de usuarios y mensajes creadas exitosamente")