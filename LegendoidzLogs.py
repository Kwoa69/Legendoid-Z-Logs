import time
import requests
import json
import os


def read_config(config_path):
    with open(config_path, 'r') as config_file:
        config = json.load(config_file)
    return config


config_path = 'config.json'
config = read_config(config_path)


last_messages = {item['path']: "" for item in config['files']}

def update_and_notify(file_path, webhook):
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
            message = lines[-1].strip()

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


for item in config['files']:
    update_and_notify(item['path'], item['webhook'])

# Lecture de la boucle 
while True:
    time.sleep(10)
    for item in config['files']:
        update_and_notify(item['path'], item['webhook'])
