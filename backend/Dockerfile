# backend/Dockerfile

FROM python:3.9-slim

WORKDIR /app

# Copier les fichiers de configuration
COPY requirements.txt requirements.txt

# Installer les dépendances
RUN pip install -r requirements.txt

# Copier le code source
COPY . .

CMD ["python", "app.py"]
