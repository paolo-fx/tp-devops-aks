# TP DevOps AKS

Description : API Flask de démonstration déployée sur Azure AKS

## Lancer l'application en local

    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements-dev.txt
    python app.py

## Bilan DevOps

### Chaîne de déploiement

Git push
  ↓
GitHub / Pull Request
  ↓
GitHub Actions
  ├── flake8 : qualité du code
  ├── pytest : tests et couverture >= 80 %
  └── Docker : build et publication
  ↓
GitHub Container Registry (GHCR)
  ↓
kubectl apply
  ↓
Azure Kubernetes Service (AKS)
  ↓
Deployment / ReplicaSet
  ↓
Service ClusterIP
  ↓
Pods Flask

### Principes 12-Factor App appliqués

- Codebase : code centralisé dans GitHub.
- Dependencies : dépendances déclarées dans requirements.txt.
- Config : configuration externalisée dans une ConfigMap.
- Build, release, run : image Docker versionnée et déployée.
- Processes : application sans état persistant.
- Port binding : API accessible sur le port 8080.
- Concurrency : plusieurs Pods et workers Gunicorn.
- Disposability : Pods recréés et rolling updates.
- Logs : journaux accessibles via kubectl logs.

### Validation

Le nouveau message V2 a été déployé automatiquement
après la fusion de la Pull Request n°7.

Le pipeline GitHub Actions a réalisé les tests,
la publication de l'image et le déploiement sur AKS.

L'accès HTTP a été vérifié avec kubectl port-forward.
L'accès externe par Ingress n'a pas été validé.