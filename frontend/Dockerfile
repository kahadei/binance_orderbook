FROM ubuntu:latest
LABEL authors="user"

ENTRYPOINT ["top", "-b"]


FROM node:18-alpine as build
WORKDIR /home/app/frontend
ADD *.json ./
RUN npm install

ADD ./public ./public
ADD ./src ./src
COPY . .