FROM node:18 as node-base

WORKDIR /app

COPY package*.json ./

RUN npm install

COPY . .

FROM python:3.10-slim as python-base

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY --from=node-base /app .

EXPOSE 3000

CMD ["node", "app.js"]