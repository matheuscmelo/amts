FROM node:12.13.1 as builder
WORKDIR /usr/src/app
COPY package.json ./
RUN npm install
COPY . .
RUN npm run build
RUN cd dist && ls

FROM nginx:1.17.1-alpine
COPY --from=builder /usr/src/app/nginx/nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=builder /usr/src/app/dist/frontend /usr/share/nginx/html
