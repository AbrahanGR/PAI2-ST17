import psycopg2
from psycopg2 import sql

#NOTAS PARA INCLUIR EN LA MEMORIA (y comentarios)
# bibliografía: https://www.psycopg.org/docs/
# Se eligió Postgres porque... (seguridad)
# Conexión a la base de datos postgres (base de datos por defecto) para crear la base de datos del servidor
# Se crearán dos usuarios: uno que será el administrador de la base de datos, al que se le asignará "OWNER" para crear las tablas y modificarlas mas adelante (mantenimiento, migracion)
# Y el otro usuario para manejar la base de datos que solo tenga acceso a leer y escribir, asi si un atacante obtiene acceso al servidor no podrá hacer modificaciones a la estructura de la db
# Hecho en un script de python para manejejar desde python y no sea necesario usar archivos .sql o algun cliente de Postgres
# Al ejecutar este script se tendrá la base de datos completamente preparada para usarse
# En la práctica este script solo se usará una vez al principio y debe quedar fuera de alcance para evitar que atacantes usen este script con fines maliciosos, ya que contiene operaciones con el superusuario postrgres
# Este script solo está hecho por comodidad para la PAI pero no sería el modo más "seguro" de crear la base de datos
connection = psycopg2.connect(
    host="localhost",
    port=5432,
    database="postgres",
    user="postgres",
    password="root" #cambiar contraseña por la definida al instalar Postgres
)
connection.autocommit = True
cursor = connection.cursor()

#Consulta segura, evita SQLi. Identifier sirve para las columnas y otros identificadores y los valores se introducen mediante "%s" y se pasan como argumento de execute en forma de tupla
cursor.execute(sql.SQL("CREATE USER {} WITH PASSWORD %s;").format(sql.Identifier("admin")), ('admin_PAI1-ST17',)) #En la práctica la contraseña deberá ser segura

cursor.execute(sql.SQL("CREATE USER {} WITH PASSWORD %s;").format(sql.Identifier("server")), ('server_PAI1-ST17',)) #En la práctica la contraseña deberá ser segura

cursor.execute(sql.SQL("CREATE DATABASE {} OWNER {}").format(sql.Identifier("PAI1-ST17"), sql.Identifier("admin")))

cursor.close()
connection.close()

print("Usuarios y base de datos creados exitosamente")