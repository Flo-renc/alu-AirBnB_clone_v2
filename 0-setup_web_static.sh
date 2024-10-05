#!/usr/bin/env bash
#script to set up web servers for web_static deployment

sudo apt-get update
sudo apt-get install -y nginx

sudo mkdir -p /data/web_static/releases/test/
sudo mkdir -p /data/web_static/shared/
echo "<html>
    <head>
    </head>
    <body>
    	Holberton School
    </body>
</html>" | sudo tee /data/web_static/releases/test/index.html

if [ -L /data/web_static/current ]; then
	sudo rm /data/web_static/current
fi
sudo ln -s /data/web_static/releases/test/ /data/web_static/current

sudo chown -R ubuntu:ubuntu /data/

sudo sed -i '/server_name _;/a \\\n\tlocation /hbnb_static/ {\n\t\talias /data/web_static/current/;\n\t}' /etc/nginx/sites-available/default

sudo service nginx restart
exit 0
