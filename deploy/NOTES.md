# NGINX configurations  for one template file HTML/CSS/JS
### works 100%
```nginx
server {  # Fix "erver" → "server"
    listen 80;
    server_name 54.166.6.159;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}

```
# NGINX configurations  for one statics file HTML/CSS/JS serrated
### works 20% serve just html
```nginx
server {
    listen 80;
    server_name your_domain.com;

    location /static/ {
        alias /path/to/your/project/staticfiles/;
    }

    location /media/ {
        alias /path/to/your/project/media/;
    }

    # Pass requests to the Django app (via Gunicorn or uWSGI)
    location / {
        proxy_pass http://127.0.0.1:8000;  # Change this to your Gunicorn or uWSGI server address
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```