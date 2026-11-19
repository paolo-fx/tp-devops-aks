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

## Incident n°4 — Régression détectée par le pipeline CI

- **Partie / étape :** Partie 3.3 — Test volontaire d'échec de la CI.
- **Symptôme observé :** Le job `Qualité et tests` échoue après le commit `fix: simplification`.
- **Diagnostic :** La modification de la fonction `est_bissextile` supprime la règle de divisibilité par 400, ce qui provoque l'échec des tests correspondant aux années 1600 et 2000.
- **Cause racine :** Régression introduite volontairement dans la logique métier.
- **Correction appliquée :** Annulation du commit défectueux avec `git revert`, suivie d'un nouveau push.
- **Comment l'éviter à l'avenir :** Conserver les tests automatisés dans le pipeline et exiger leur réussite avant toute fusion dans `main`.

## Incident n°5 — Dépassement mémoire des Pods Kubernetes

- **Partie / étape :** Partie 4.2 — Déploiement Kubernetes sur AKS.
- **Symptôme observé :** Les deux Pods restent à `0/1 Ready`, avec des états `OOMKilled` et `CrashLoopBackOff`.
- **Diagnostic :** Consultation des Pods, de leurs événements et du quota avec `kubectl get pods -w`, `kubectl describe pods`, `kubectl get events` et `kubectl describe resourcequota`.
- **Cause probable :** La limite de mémoire de 32 MiB est insuffisante pour exécuter l'application Flask avec deux workers Gunicorn.
- **Correction appliquée :** Augmentation de `requests.memory` de 16 MiB à 64 MiB et de `limits.memory` de 32 MiB à 128 MiB, sans modifier les valeurs CPU.
- **Justification :** Le namespace dispose d'un quota de 2 GiB de mémoire en limites. Deux Pods à 128 MiB utilisent au maximum 256 MiB selon leurs limites déclarées.
- **Vérification :** À compléter après le nouveau déploiement.
- **Prévention :** Mesurer la consommation mémoire et définir des ressources adaptées avant la mise en production.

## Incident n°6 — Mise à jour Kubernetes défectueuse et rollback

- **Partie / étape :** Partie 4.7 — Mise à jour et retour arrière.
- **Symptôme observé :** Un nouveau Pod reste en `ImagePullBackOff` après une tentative de mise à jour.
- **Diagnostic :** Les commandes `kubectl get pods` et `kubectl rollout history deployment/mon-app` montrent qu'une nouvelle révision utilise une image inexistante.
- **Cause racine :** Utilisation volontaire du tag Docker `n-existe-pas`, qui n'existe pas dans GHCR.
- **Impact :** Les deux anciens Pods sont restés opérationnels pendant l'échec de la mise à jour.
- **Correction appliquée :** Exécution de `kubectl rollout undo deployment/mon-app` pour revenir à la révision précédente.
- **Résultat :** Le rollback a réussi et le Pod défectueux est passé en cours de suppression.
- **Prévention :** Vérifier l'existence des images avant déploiement et utiliser des tags SHA précis. Conserver les sondes de disponibilité et la stratégie RollingUpdate.