FROM openjdk:17-jdk-slim

WORKDIR /app/java

ADD https://dev.mysql.com/get/Downloads/Connector-J/mysql-connector-j-9.0.0.tar.gz /tmp/
RUN tar -xvzf /tmp/mysql-connector-j-9.0.0.tar.gz -C /tmp && \
    mv /tmp/mysql-connector-j-9.0.0/mysql-connector-j-9.0.0.jar /app/java/

COPY jdbc/src /app/java/src

RUN mkdir -p /app/java/bin

RUN javac -cp "/app/java/mysql-connector-j-9.0.0.jar" -d /app/java/bin /app/java/src/*.java

RUN apt-get update && \
    apt-get install -y curl && \
    curl -fsSL https://deb.nodesource.com/setup_16.x | bash - && \
    apt-get install -y nodejs && \
    apt-get clean

WORKDIR /app/node

COPY package*.json ./

RUN npm install

COPY . .

EXPOSE 3000

CMD ["node", "app.js"]