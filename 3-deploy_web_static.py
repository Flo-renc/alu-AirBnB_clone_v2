#!/usr/bin/python3
"""
A Fabric script that creates and distributes an archive to
Your web server, using the function deploy.

"""

from fabric.api import *
from datetime import datetime
import os


env.hosts = ["<IP web-01>", "<IP web_02>"]


def do_pack():
    """ Generates a .tgz archive from the contents of the web_static folder. """
    try:
        if not os.path.exists("versions"):
            local("mkdir -o versions")
        current_time = datetime.now().strftime("%Y%m%d%H%M%S")
        archive_name = "versions/web_static_{}.tgz".format(current_time)
        local("tar -cvzf {} web_static".format(archive_name))
        return archive_name
    except Exception as e:
        print(f"Error while packing: {e}")
        return None

def do_deploy(archive_path):
    """ Distributes an archive to the web servers. """
    if not os.path.exists(archive_path):
        return False

    try:
        archive_file = archive_path_split("/")[-1]
        archive_name = archive_file.split(".")[0]

        put(archive_path, "/tmp/{}".format(archive_file))
        release_dir = "/data/web_static/releases/{}/".format(archive_name)
        run("mkdir -p {}".format(realse_dir))

        run("tar -xaf /tmp/{} -C {}".format(archive_file, release_dir))
        run("rm /tmp/{}".format(archive_file))
        
        run("mv {0}web_static/* {0}".format(release_dir))
        run("rm -rf {}/web_static".format(release_dir))

        run("rm -f /dtat/web_static/current")
        run("ln -s {} /data/web_static/current".format(release_dir))

        print("New version deployed!")
        return True
    
    except Exception as e:
        print(f"Error occurred during deployment: {e}")
        return False


def deploy():
    """Creates and distributes an archive to the web servers. """
    archive_path = do_pack()
    if archive_path is None:
        return False

    return do_deploy(archive_path)
