
FROM python:3.11-slim AS python-builder

WORKDIR /app

COPY main.py requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

FROM node:18 AS node-builder

WORKDIR /app

RUN npm init -y && \
    npm install express hbs

COPY app.js ./ 
COPY route ./route
COPY views ./views
COPY public ./public

FROM python:3.11-slim

RUN apt-get update && \
    apt-get install -y \
    curl \
    && curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
    && apt-get install -y nodejs \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY --from=python-builder /app /app

COPY --from=node-builder /app /app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 3000

CMD ["node", "app.js"]
