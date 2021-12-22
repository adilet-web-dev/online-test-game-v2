FROM node:lts-slim

WORKDIR /app



RUN apt-get update

COPY package*.json ./

RUN npm install

COPY . .

RUN npm install -g http-server

RUN npm run build

EXPOSE 8080

CMD [ "http-server", "dist" ]
