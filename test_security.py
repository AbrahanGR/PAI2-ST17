

import unittest
import socket
import time
import client_login  
import server_login  

HOST = '127.0.0.1'
PORT = 3030

# Nome utente da testare
username = 'TestUser'

# password para el test
passwords = ['password1', '12345', 'TestPassword', 'password123', 'admin','abcdeg','Test']

class TestSecurity(unittest.TestCase):

    # test del brute force
    def test_brute_force_login(self):
        print("Simulando Brute Force Attack...")
        for password in passwords:
            # Crea el mensaje de login
            message = f"1,{username},{password}"
            
            # envia el mensaje de login al server
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((HOST, PORT))
                s.send(message.encode())  # envia el intento de login
                response = s.recv(1024).decode()  #  respuesta dal servidor  
                print(f"intentando login con la password: {password} | Respuesta: {response}")

                # Si logramos el login 
                if "Inicio de sesión exitoso" in response:
                    print(f"Brute-force success! La password correcta es: {password}")
                    self.assertEqual(response, "Inicio de sesión exitoso")  # Verifica la risposta
                    return password  

    #test del replay attack
    def test_replay_attack(self):
        print("Simulando Replay Attack...")
        for password in passwords:
            # Criando el mensaje de login
            message = f"1,{username},{password}"
            
            # antes enviamo el mensaje
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((HOST, PORT))
                s.send(message.encode())  # Invia il tentativo di login
                response = s.recv(1024).decode()  # Ricevi la risposta dal server
                print(f"Tentativo de login con la password {password} | Respuesta: {response}")
            
            # lo enviamos otra vez para testar el replay
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((HOST, PORT))
                s.send(message.encode())  # Invia il tentativo di login ripetuto
                response = s.recv(1024).decode()  # Ricevi la risposta dal server
                print(f"Tentativo de login (Replay) con la password {password} | Respuesta: {response}")
                self.assertNotEqual(response, "Inicio de sesión exitoso")  # Assicurati che la risposta sia diversa per un replay

    # il test del MITM (Man-in-the-Middle)
    def test_mitm_attack(self):
        print("Simulazione Man-in-the-Middle Attack...")
        for password in passwords:
            # mensaje original
            original_message = f"1,{username},{password}"

            # cambiamo la password
            tampered_password = "tampered_password"  # Modifica el mensaje
            tampered_message = f"1,{username},{tampered_password}"
            
            # envia el mensaje original al server
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((HOST, PORT))
                s.send(original_message.encode())  # enviamos el mensaje original
                response = s.recv(1024).decode()  
                print(f"Tentativo de login original con la password {password} | Respuesta: {response}")
            
            # ora enviamos el mensaje cambiado (MITM) al server
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((HOST, PORT))
                s.send(tampered_message.encode())  # enviamos el mensaje cambiado
                response = s.recv(1024).decode()  
                print(f"Tentativo de login (MITM) con la password {tampered_password} | Respuesta: {response}")
                self.assertNotEqual(response, "Inicio de sesión exitoso")  # Assicurati che la risposta sia diversa per un MITM

if __name__ == "__main__":
    unittest.main()
