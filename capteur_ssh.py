import socket
import threading
import redis
import pandas as pd
from datetime import datetime
import time

# Configuration des ports pour les capteurs
ports = {
    "front_range": 6000,
    "back_range": 6001,
    "right_range": 6002,
    "left_range": 6003
}

# Connexion à Redis
redis_client = redis.StrictRedis(host="localhost", port=6379, db=0)

# Fonction pour gérer les connexions entrantes pour un capteur
def serveur_tcp(port, capteur):
    print(f"Serveur actif pour {capteur} sur le port {port}...")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("0.0.0.0", port))
        s.listen(5)
        while True:
            conn, addr = s.accept()
            with conn:
                data = conn.recv(1024).decode("utf-8").strip()
                for message in data.split("\n"):
                    if message:
                        try:
                            # Parse les données reçues
                            _, timestamp, valeur = message.split(",")
                            timestamp = float(timestamp)
                            valeur = int(valeur)

                            # Ajouter la donnée dans Redis (Sorted Set)
                            redis_key = f"capteur:{capteur}"
                            redis_client.zadd(redis_key, {f"{timestamp}:{valeur}": timestamp})

                            print(f"[{capteur}] Donnée insérée : {timestamp}, {valeur}")
                        except ValueError:
                            print(f"Donnée mal formée reçue pour {capteur} : {message}")

# Fonction pour exporter les données Redis dans un fichier CSV avec Pandas
def exporter_donnees_redis_pandas():
    all_data = []
    for capteur in ports.keys():
        redis_key = f"capteur:{capteur}"
        valeurs = redis_client.zrange(redis_key, 0, -1, withscores=True)
        
        for val, _ in valeurs:
            timestamp, valeur = val.decode("utf-8").split(":")
            all_data.append({
                "Capteur": capteur,
                "Timestamp": datetime.fromtimestamp(float(timestamp)).strftime("%Y-%m-%d %H:%M:%S"),
                "Valeur": int(valeur)
            })

    # Créer un DataFrame Pandas
    df = pd.DataFrame(all_data)

    # Sauvegarder les données dans un fichier CSV
    df.to_csv("donnees_capteurs.csv", index=False)
    print("Données sauvegardées dans donnees_capteurs.csv")

# Fonction pour sauvegarder périodiquement les données
def sauvegarde_periodique(intervale):
    while True:
        exporter_donnees_redis_pandas()
        time.sleep(intervale)

# Lancer un thread pour chaque capteur
threads = []
for capteur, port in ports.items():
    thread = threading.Thread(target=serveur_tcp, args=(port, capteur))
    thread.start()
    threads.append(thread)

# Thread pour la sauvegarde automatique toutes les heures (10 secondes)
thread_sauvegarde = threading.Thread(target=sauvegarde_periodique, args=(10,))
thread_sauvegarde.start()
threads.append(thread_sauvegarde)

# Attendre la fin des threads (infinie dans ce cas)
for thread in threads:
    thread.join()
