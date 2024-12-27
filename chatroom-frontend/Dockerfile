## node
FROM node:20.11.1-alpine AS build

WORKDIR /usr/src/app

COPY package*.json ./

RUN --mount=type=cache,target=/usr/src/app/.npm \
    npm set cache /usr/src/app/.npm && \
    npm ci

COPY . .

RUN npm run build

## nginx
FROM nginxinc/nginx-unprivileged:alpine3.20-slim

COPY ./nginx/proxy_params ./nginx/default.conf.tpl /etc/nginx/
COPY ./nginx/start_nginx.sh ./
COPY --link --from=build /usr/src/app/dist /usr/share/nginx/html

USER root

RUN touch /etc/nginx/conf.d/default.conf && \
    mkdir -p /etc/nginx/ssl && chown nginx:nginx -R /etc/nginx/ssl && \
    chown nginx:nginx /etc/nginx/conf.d/default.conf && \
    chmod +x ./start_nginx.sh
# production
# COPY ./nginx/ssl/fullchain.pem /etc/nginx/ssl/fullchain.pem
# COPY ./nginx/ssl/privkey.pem /etc/nginx/ssl/privkey.pem

VOLUME /etc/nginx/ssl

USER nginx

EXPOSE 443

ENTRYPOINT ["sh", "-c", "./start_nginx.sh"]