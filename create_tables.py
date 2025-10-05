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
    database="PAI1-ST17",
    user="admin",
    password="admin_PAI1-ST17"
)

connection.autocommit = True
cursor = connection.cursor()

cursor.execute("DROP TABLE IF EXISTS users")
cursor.execute("CREATE TABLE users (username VARCHAR(255) PRIMARY KEY, password VARCHAR(128))")

#Introducir usuarios prerregistrados
hash1 = hashing.hash_password("P3p3*sEgUrO*1nd3sc1fr4bl3")
hash2 = hashing.hash_password("PEpA_s3gur4_IndEscIfRAblE")
server_login.store_new_user("pepe", hash1, connection)
server_login.store_new_user("pepa", hash2, connection)

cursor.execute("DROP TABLE IF EXISTS transactions")
cursor.execute("CREATE TABLE transactions (origin VARCHAR(255) NOT NULL, dst VARCHAR(255) NOT NULL, amount INT, nonce VARCHAR(255) PRIMARY KEY)")

#cursor.execute("CREATE TABLE IF NOT EXISTS transactions (origin VARCHAR(255) NOT NULL, dst VARCHAR(255) NOT NULL, amount INT, nonce INT PRIMARY KEY)")

#Le damos permisos de lectura, escritura y edición de los datos sobre las tablas
cursor.execute(sql.SQL("GRANT SELECT, INSERT, UPDATE ON ALL TABLES IN SCHEMA public TO {};").format(sql.Identifier("server")))

cursor.execute(sql.SQL("GRANT USAGE ON ALL SEQUENCES IN SCHEMA public TO {};").format(sql.Identifier("server")))

cursor.close()
connection.close()

print("Tablas de usuarios y transacciones creadas exitosamente")