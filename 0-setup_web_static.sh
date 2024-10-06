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

if ! sudo sed -i '/server_name _;/a location /hbnb_static/ {\n\talias /data/web_static/current/;\n}' /etc/nginx/sites-available/default; then
	    echo "Failed to update Nginx configuration"
	    exit 1
fi

if ! sudo nginx -t; then
	echo "Nginx configuration test failed"
	exit 1
fi

sudo service nginx restart
exit 0
