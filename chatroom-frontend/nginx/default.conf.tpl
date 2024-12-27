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
    client_max_body_size 10M;

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

    location @proxy_api {
        include /etc/nginx/proxy_params;
        proxy_pass http://django;
    }
}

server {
    listen ${DJ_PORT};
    server_name ${DOMAIN};

    location / {
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