#!/bin/bash

# Update system packages
sudo apt update -y
sudo apt upgrade -y

# Install Python and pip
sudo apt install -y python3 python3-pip python3-dev

# Install MySQL
sudo apt install -y mysql-server

# Install MySQL client
sudo apt install -y libmysqlclient-dev

# Install pip packages from requirements.txt
pip3 install -r ~/CutProjects/Alsalam_Furniture-moving/requirements.txt

# Setup MySQL (optional, set up your MySQL root password and create the database)
sudo mysql_secure_installation

# Create a MySQL user and database for your project
mysql -u root -p -e "
CREATE DATABASE Alsalam_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'salam_admin'@'localhost' IDENTIFIED BY 'peace_25_pwd';
GRANT ALL PRIVILEGES ON Alsalam_db.* TO 'salam_admin'@'localhost';
FLUSH PRIVILEGES;
"

# Start MySQL service on Ubuntu
sudo service mysql start

# Check if everything is installed properly
python3 --version
pip3 --version
django-admin --version
mysql --version

echo "Setup is complete!"
