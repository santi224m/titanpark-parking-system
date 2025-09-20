# Server Setup Guide

**OS:** Ubuntu 24.04.3 LTS

## Update and install software

```bash
sudo apt update
sudo apt upgrade
sudo apt install -y python3 python3-pip python3-venv postgresql nginx git
```

## Create ```deploy``` user

* As root user

```bash
sudo adduser deploy
sudo usermod -aG sudo deploy
```

Logout as root and login as deploy user when done

## Set up SSH key authentication for deploy user

* Run this on local machine

```bash
ssh-keygen -t rsa -b 4096 -f ~/.ssh/titanpark_deploy -N ""
ssh-copy-id -i ~/.ssh/titanpark_deploy.pub deploy@server-ip
```

## Create application directory and git clone repo

```bash
sudo mkdir -p /opt/titanpark
sudo chown deploy:deploy /opt/titanpark
cd /opt/titanpark
git clone https://github.com/santi224m/titanpark-parking-system.git
cd titanpark-parking-system/
```

## Make ```deploy.sh``` executable

```bash
chmod +x /opt/titanpark/titanpark-parking-system/server/deploy.sh
/opt/titanpark/titanpark-parking-system/server/deploy.sh
```

## Setup systemd service

```bash
sudo cp /opt/titanpark/titanpark-parking-system/server/titanpark.service /etc/systemd/system/titanpark.service
sudo systemctl daemon-reload
sudo systemctl enable titanpark
sudo systemctl start titanpark
```

## Setup nginx

```bash
sudo cp /opt/titanpark/titanpark-parking-system/server/titanpark.nginx /etc/nginx/sites-available/titanpark
sudo ln -s /etc/nginx/sites-available/titanpark /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

## Set Up GitHub Secrets

In GitHub repo, go to ```Settings → Secrets and variables → Actions```, and add:

* ```HOST```: Linode server IP address
* ```USERNAME```: ```deploy```
* ```SSH_KEY```: Contents of your private key (~/.ssh/titanpark_deploy)