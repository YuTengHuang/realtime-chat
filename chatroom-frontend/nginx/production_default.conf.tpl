map ${DOLLAR}http_upgrade ${DOLLAR}connection_upgrade {
    default upgrade;
    '' close;
}

upstream django {
    server ${DJ_HOST}:${DJ_PORT};
}

server {
    listen 8000;
    server_name ${DOMAIN};
    return 301 https://${DOLLAR}host${DOLLAR}request_uri;
}

server {
    listen 443 ssl;
    http2 on;
    server_name ${DOMAIN};
    client_max_body_size  1M;
    ssl_certificate /etc/nginx/ssl/fullchain.pem;
    ssl_certificate_key /etc/nginx/ssl/privkey.pem;
    ssl_protocols TLSv1 TLSv1.1 TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    resolver 127.0.0.11;


    location / {
        root /usr/share/nginx/html;
        index index.html;
        try_files ${DOLLAR}uri ${DOLLAR}uri/ /index.html;
    }

    location /api {
        try_files ${DOLLAR}uri @proxy_api;
    }

    location /ws/chat_rooms {
        try_files ${DOLLAR}uri @proxy_api;
    }

    location /admin {
        try_files ${DOLLAR}uri @proxy_api;
    }

    location @proxy_api {
        include /etc/nginx/proxy_params;
        proxy_pass http://django;
    }
}