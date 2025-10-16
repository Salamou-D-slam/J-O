FROM python:3.13-slim

WORKDIR /app

# Installez les dépendances système nécessaires
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Mettre à jour pip
RUN pip install --upgrade pip

# Copiez et installez les dépendances Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir gunicorn

# Copiez le reste du code
COPY . .

# Exposez le port 5000
EXPOSE 5000

# Commande pour démarrer l'application
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "main:app"]
