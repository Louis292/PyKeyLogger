import socket
import threading
from datetime import datetime

# Configuration du serveur
HOST = '127.0.0.1'  # Adresse IP locale
PORT = 12346  # Port du serveur

def log_server_message(message):
    """Enregistre les messages dans un fichier logs_server.txt."""
    timestamp = get_current_time()  # Récupérer l'heure actuelle
    log_message = f"[{timestamp}] {message}\n"
    with open("logs_server.txt", "a") as log_file:
        log_file.write(log_message)

def get_current_time():
    """Retourne la date et l'heure actuelles au format jour/mois/année heure:minute:seconde."""
    now = datetime.now()
    return now.strftime("%d/%m/%Y %H:%M:%S")

def handle_client(client_socket):
    """Fonction pour gérer les connexions des clients."""
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break
            print(f"Client > {message}")

            # Log du message côté serveur
            log_server_message(f"Message reçu de {client_socket.getpeername()}: {message}")

        except Exception as e:
            print(f"Erreur : {e}")
            break

    print("Client déconnecté.")
    client_socket.close()

def start_server():
    """Démarre le serveur et gère les connexions clients."""
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(5)  # Maximum de clients en attente

    print(f"Serveur démarré sur {HOST}:{PORT}")

    try:
        while True:
            client_socket, addr = server.accept()
            print(f"Connexion acceptée depuis {addr}")
            client_handler = threading.Thread(target=handle_client, args=(client_socket,))
            client_handler.start()

    except KeyboardInterrupt:
        print("\nArrêt du serveur...")
    finally:
        server.close()

def stop_server():
    """Fonction pour arrêter le serveur."""
    print("Serveur arrêté.")

# Démarre le serveur dans un thread
server_thread = threading.Thread(target=start_server)
server_thread.start()

# Attend que l'utilisateur tape 'quit' pour arrêter le serveur
while True:
    command = input("Tapez 'quit' pour arrêter le serveur : ")
    if command == 'quit':
        stop_server()
        break
