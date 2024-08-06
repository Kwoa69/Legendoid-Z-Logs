import time
import requests
import json
import glob
import os

def read_config(config_path):
    """Lit le fichier de configuration JSON et retourne le dictionnaire correspondant."""
    with open(config_path, 'r') as config_file:
        config = json.load(config_file)
    return config

def find_dynamic_file(pattern):
    """Trouve le fichier le plus récent correspondant au motif donné."""
    files = glob.glob(pattern)  
    if not files:
        return None
    return max(files, key=os.path.getctime)  

def update_and_notify(file_path, webhook, last_messages):
    """Lit le dernier message d'un fichier et envoie une notification à Discord si le message a changé."""
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
            message = lines[-1].strip()

        if file_path not in last_messages:
            last_messages[file_path] = ""  

        if message != last_messages[file_path]:
            message_with_warning = f"{message} - **Legendoid'Z Logs**"
            payload = {"content": message_with_warning}
            headers = {"Content-Type": "application/json"}

            response = requests.post(webhook, data=json.dumps(payload), headers=headers)

            if response.status_code == 204:
                print(f"Message sent to Discord for {file_path}: {message_with_warning}")
                last_messages[file_path] = message
            else:
                print(f"Failed to send message to Discord for {file_path}: {response.status_code} {response.text}")
    except Exception as e:
        print(f"Error reading file {file_path} or sending message: {e}")

def main():
    config_path = 'config.json'
    config = read_config(config_path)

    # Dictionnaire pour stocker les derniers messages lus
    last_messages = {}

    # Boucle de lecture et de notification
    while True:
        # Traiter les fichiers de la configuration
        for item in config['files']:
            if '*' in item['path']:  # Vérifie si le chemin est un motif dynamique
                dynamic_file = find_dynamic_file(item['path'])
                if dynamic_file:
                    update_and_notify(dynamic_file, item['webhook'], last_messages)
                else:
                    print(f"No dynamic file found for pattern: {item['path']}")
            else:
                if os.path.exists(item['path']):
                    update_and_notify(item['path'], item['webhook'], last_messages)
                else:
                    print(f"File not found: {item['path']}")

        # Pause entre chaque cycle de vérification
        time.sleep(10)

if __name__ == "__main__":
    main()
