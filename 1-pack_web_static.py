#!/usr/bin/python3
"""
A Fabric script that generates a
.tgz archive from the contents of the web_static folder of your
AirBnB Clone repo, using the function do_pack

"""

from fabric.api import local
from datetime import datetime
import os


def do_pack():
    """ the do_pack function generates a .tgz archive 
    from the contents of the web_static folder """
    if not os.path.exists("versions"):
        os.makedirs("versions")

    current_time = datetime.now()
    current_time_str = current_time.strftime("%Y%m%d%H%M%S")
    
    archive_path = "versions/web_static_{}.tgz".format(current_time_str)
    result = local("sudo tar -cvzf {} web_static".format(archive_path))

    if result.succeeded:
        file_size = os.path.getsize(archive_path)
        print("Archive created: {} | size: {} bytes".
                format(archive_path, file_size))
        return archive_path
    else:
        print("Failed to create arcive")
        return None
