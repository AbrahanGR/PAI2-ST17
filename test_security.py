

import unittest
import socket
import time
import client_login  
import server_login  

# Indirizzo e porta del server
HOST = '127.0.0.1'
PORT = 3030

# Nome utente da testare
username = 'TestUser'

# Lista di password da testare
passwords = ['password1', '12345', 'TestPassword', 'password123', 'admin','abcdeg','Test']

class TestSecurity(unittest.TestCase):

    # Funzione per il test del brute force
    def test_brute_force_login(self):
        print("Simulazione Brute Force Attack...")
        for password in passwords:
            # Crea il messaggio di login
            message = f"1,{username},{password}"
            
            # Invia il messaggio di login al server
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((HOST, PORT))
                s.send(message.encode())  # Invia il tentativo di login
                response = s.recv(1024).decode()  # Ricevi la risposta dal server
                print(f"Tentativo di login con la password {password} | Risposta: {response}")

                # Se il login ha successo, fermiamo il brute force
                if "Inicio de sesión exitoso" in response:
                    print(f"Brute-force successo! La password corretta è: {password}")
                    self.assertEqual(response, "Inicio de sesión exitoso")  # Verifica la risposta
                    return password  # Restituiamo la password corretta

    # Funzione per il test del replay attack
    def test_replay_attack(self):
        print("Simulazione Replay Attack...")
        for password in passwords:
            # Crea il messaggio di login
            message = f"1,{username},{password}"
            
            # Prima inviamo il messaggio
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((HOST, PORT))
                s.send(message.encode())  # Invia il tentativo di login
                response = s.recv(1024).decode()  # Ricevi la risposta dal server
                print(f"Tentativo di login con la password {password} | Risposta: {response}")
            
            # Ora inviamo lo stesso messaggio una seconda volta per testare il replay
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((HOST, PORT))
                s.send(message.encode())  # Invia il tentativo di login ripetuto
                response = s.recv(1024).decode()  # Ricevi la risposta dal server
                print(f"Tentativo di login (Replay) con la password {password} | Risposta: {response}")
                self.assertNotEqual(response, "Inicio de sesión exitoso")  # Assicurati che la risposta sia diversa per un replay

    # Funzione per il test del MITM (Man-in-the-Middle)
    def test_mitm_attack(self):
        print("Simulazione Man-in-the-Middle Attack...")
        for password in passwords:
            # Crea il messaggio di login originale
            original_message = f"1,{username},{password}"

            # Simuliamo un attacco MITM alterando la password
            tampered_password = "tampered_password"  # Modifica il messaggio
            tampered_message = f"1,{username},{tampered_password}"
            
            # Invia il messaggio originale al server
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((HOST, PORT))
                s.send(original_message.encode())  # Invia il tentativo di login originale
                response = s.recv(1024).decode()  # Ricevi la risposta dal server
                print(f"Tentativo di login originale con la password {password} | Risposta: {response}")
            
            # Ora inviamo il messaggio modificato (MITM) al server
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((HOST, PORT))
                s.send(tampered_message.encode())  # Invia il tentativo di login alterato
                response = s.recv(1024).decode()  # Ricevi la risposta dal server
                print(f"Tentativo di login (MITM) con la password {tampered_password} | Risposta: {response}")
                self.assertNotEqual(response, "Inicio de sesión exitoso")  # Assicurati che la risposta sia diversa per un MITM

if __name__ == "__main__":
    unittest.main()
