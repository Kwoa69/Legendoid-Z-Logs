### Legendoid-Z-Logs


Ce script en Python permet de surveiller des fichiers log spécifiques et d'envoyer des notifications à des webhooks Discord lorsque de nouvelles entrées sont détectées.

Vous pouvez configurer plusieurs fichiers log et webhooks Discord pour recevoir les notifications.

Pré-requis

- Webhook Discord

Avant d'utiliser ce script, assurez-vous d'avoir installé les dépendances suivantes :
- Python 3.x
- Bibliothèque requests

Pour installer les dépendances : 

```pip install requests```

- Ajuster le fichier  ```config.json```

Pour lancer le script : 

```python LegendoidzLogs.py```


Notes : 
- Surveillance en Temps Réel: Le script vérifie les fichiers log toutes les 10 secondes. Vous pouvez ajuster cet intervalle en modifiant la valeur ligne 46 
- Gestion des Erreurs: Le script gère les erreurs potentielles telles que la lecture des fichiers ou l'envoi des messages aux webhooks Discord.
