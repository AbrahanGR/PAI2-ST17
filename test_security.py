

import socket
import time
import client_login  # Utilizzeremo le funzioni di login del client
import server_login  # Utilizzeremo la logica di login del server

# Indirizzo e porta del server
HOST = '127.0.0.1'
PORT = 3030

# Nome utente da testare
username = 'TestUser'

# Lista di password da testare (modifica come necessario)
passwords = ['password1', '12345', 'TestPassword', 'password123', 'admin']

# Funzione per il test del brute force
def brute_force_login():
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
                return password  # Restituiamo la password corretta

# Funzione per il test del replay attack
def replay_attack():
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

# Funzione per il test del MITM (Man-in-the-Middle)
def mitm_attack():
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

if __name__ == "__main__":
    # Eseguiamo i test
    brute_force_login()  # Test Brute Force
    time.sleep(2)  # Attendi un attimo tra i test
    replay_attack()  # Test Replay Attack
    time.sleep(2)  # Attendi un attimo tra i test
    mitm_attack()  # Test Man-in-the-Middle Attack
