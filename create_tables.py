import psycopg2
from psycopg2 import sql

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

#Le damos permisos de lectura, escritura y edición de los datos

cursor.execute(sql.SQL("GRANT SELECT, INSERT, UPDATE ON ALL TABLES IN SCHEMA public TO {};").format(sql.Identifier("server")))

cursor.execute(sql.SQL("GRANT USAGE ON ALL SEQUENCES IN SCHEMA public TO {};").format(sql.Identifier("server")))

cursor.execute("CREATE TABLE users (username VARCHAR(255) PRIMARY KEY, password VARCHAR(128))")
cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", ('pepe', 'prueba'))
cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", ('pepa', 'prueba2'))

cursor.execute("CREATE TABLE transactions (origin VARCHAR(255) NOT NULL, dst VARCHAR(255) NOT NULL, amount FLOAT, PRIMARY KEY (origin, dst))")

cursor.close()
connection.close()

print("Tablas de usuarios y transacciones creadas exitosamente")