FROM openjdk:17-jdk-slim

WORKDIR /app

ADD https://dev.mysql.com/get/Downloads/Connector-J/mysql-connector-j-9.0.0.tar.gz /tmp/

RUN tar -xvzf /tmp/mysql-connector-j-9.0.0.tar.gz -C /tmp && \
    mv /tmp/mysql-connector-j-9.0.0/mysql-connector-j-9.0.0.jar /app/

COPY jdbc/src/*.java /app/

RUN javac -cp "/app/mysql-connector-j-9.0.0.jar" *.java

FROM node:12.18.1

WORKDIR /app

COPY package*.json ./
 
RUN npm install
 
COPY . .

EXPOSE 3000

CMD [ "node","app.js" ]