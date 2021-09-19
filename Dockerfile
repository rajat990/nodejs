FROM node:alpine
WORKDIR /usr/app
COPY ./package.json ./
RUN  npm install
RUN npm install -g nodemon
COPY ./ ./
CMD ["npm","start" ]