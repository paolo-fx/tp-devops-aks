# Journal des incidents — TP DevOps AKS

## Incident n°1 — Conflit de nom du conteneur Docker

- **Partie / étape :** Partie 2 — Exécution Docker.
- **Symptôme observé :** La commande `docker run` échoue avec le message `Conflict. The container name "/mon-app" is already in use`.
- **Diagnostic :** La commande `docker ps -a` permet de constater qu'un conteneur nommé `mon-app` existe déjà.
- **Cause racine :** Docker interdit la création de deux conteneurs portant le même nom.
- **Correction appliquée :** Suppression de l'ancien conteneur avec `docker rm -f mon-app`, puis création d'un nouveau conteneur.
- **Comment l'éviter à l'avenir :** Vérifier les conteneurs existants avec `docker ps -a` avant d'en créer un nouveau.

## Incident n°2 — Application Docker inaccessible depuis l'extérieur

- **Partie / étape :** Partie 2.4 — Exécution et vérification du conteneur.
- **Symptôme observé :** Les requêtes `curl localhost:8080` échouent avec l'erreur `Recv failure: Connection reset by peer`, alors que le conteneur est démarré.
- **Diagnostic :** La commande `docker history tp-devops-aks:1.0` et l'inspection du Dockerfile montrent que Gunicorn est configuré pour écouter sur `127.0.0.1:8080`.
- **Cause racine :** L'application écoute uniquement sur l'interface locale du conteneur, ce qui empêche son accès depuis l'hôte via le port Docker publié.
- **Correction appliquée :** Modification de la commande Gunicorn dans le Dockerfile pour écouter sur `0.0.0.0:8080`. Reconstruction de l'image et redémarrage du conteneur.
- **Résultat :** L'API répond correctement avec le message `Bonjour Docker`, et la route `/bissextile/2000` retourne `true`.
- **Comment l'éviter à l'avenir :** Vérifier l'adresse d'écoute du serveur et effectuer un test HTTP depuis l'extérieur du conteneur.

## Incident n°3 — Requêtes effectuées avant la disponibilité de l'application

- **Partie / étape :** Partie 2.4 — Vérification après reconstruction.
- **Symptôme observé :** Après correction du Dockerfile, les premières requêtes HTTP échouent encore. Quelques instants plus tard, elles réussissent.
- **Diagnostic :** `docker ps` indique que le conteneur fonctionne et `docker logs mon-app` confirme que Gunicorn écoute sur `0.0.0.0:8080` avec ses deux workers.
- **Cause probable :** Les premières requêtes ont été effectuées avant que l'application soit entièrement prête.
- **Correction appliquée :** Nouvelle vérification HTTP avec `curl --retry 10 --retry-delay 2 --retry-all-errors`, qui confirme le bon fonctionnement.
- **Comment l'éviter à l'avenir :** Ajouter un contrôle de disponibilité (healthcheck) et attendre que l'application soit prête avant de lancer les tests HTTP.