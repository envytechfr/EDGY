# frontend/Dockerfile

FROM node:14

WORKDIR /app

# Copier les fichiers de configuration
COPY package.json package-lock.json ./

# Installer les dépendances
RUN npm install

# Copier le code source
COPY . .

CMD ["npm", "start"]
