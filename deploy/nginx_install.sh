# Install Nginx
sudo apt install -y nginx

# Allow Nginx through firewall (if UFW is used)
# sudo ufw allow 'Nginx Full'

# Create Nginx config for your Django project (basic placeholder)
sudo tee /etc/nginx/sites-available/alsalam_project > /dev/null <<EOF
server {
    listen 80;
    server_name _;  # Replace '_' with your domain or IP if possible

    # Proxy pass for Django app (backend)
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Serve static files (e.g., CSS/JS for DRF browsable API)
    location /static/ {
        alias /home/ubuntu/Alsalam_Furniture-moving/static/;
        autoindex on;                        # Optional: allow directory listing
        access_log off;
        expires 30d;
        add_header Cache-Control "public";
    }

    # Serve media files (e.g., uploaded images)
    location /media/ {
        alias /home/ubuntu/Alsalam_Furniture-moving/media/;
        autoindex on;
        access_log off;
        expires 30d;
        add_header Cache-Control "public";
    }

    # Optional: error handling
    error_page 404 /404.html;
    error_page 500 502 503 504 /50x.html;
}

EOF

# Enable the site
sudo ln -s /etc/nginx/sites-available/alsalam_project /etc/nginx/sites-enabled/

# Remove default config if it exists
sudo rm -f /etc/nginx/sites-enabled/default

# Test and reload Nginx
sudo nginx -t && sudo systemctl reload nginx

# ----------- FINAL CHECKS ------------

# Check if everything is installed properly
python3 --version
pip3 --version
django-admin --version
mysql --version
nginx -v

echo "Deployment complete!"
# config path
# sudo vim /etc/nginx/sites-available/alsalam_project
