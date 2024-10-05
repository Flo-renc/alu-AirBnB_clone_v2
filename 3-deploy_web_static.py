#!/usr/bin/python3
"""
A Fabric script that creates and distributes an archive to
Your web server, using the function deploy.

"""

from fabric.api import env, run, put, local
from datetime import datetime
import os


env.hosts = ["54.234.22.100", "54.144.229.232"]


def do_pack():

    """ Generates a .tgz archive from the contents of the web_static folder. """
    
    try:
        if not os.path.exists("versions"):
            local("mkdir -o versions")
        current_time = datetime.now().strftime("%Y%m%d%H%M%S")
        archive_path = "versions/web_static_{}.tgz".format(current_time)
        
        result = local("tar -cvzf {} web_static".format(archive_path))
        
        if result.failed:
            return None
        return archive_path

def do_deploy(archive_path):

    """ Distributes an archive to the web servers. """

    if not os.path.exists(archive_path):
        return False
    try:
        put(archive_path, "/tmp/")
        fileName = os.path.basename(archive_path)
        name_no_ext = fileName.split('.')[0]

        run("mkdir -p /data/web_static/releases/{}/".format(name_no_ext))

        run("tar -xzf /tmp/{} -C /data/web_static/releases/{}/".format(fileName, name_no_ext))

        run("rm /tmp/{}".format(fileName))

        run("mv /data/web_static/releases/{}/web_static/* /data/web_static/releases/{}/".format(name_no_ext, name_no_ext))

        run("rm -rf /data/web_static/releases/{}/web_static".format(name_no_ext))

        run("rm -rf /data/web_static/current")

        run("ln -s /data/web_static/releases/{}/ /data/web_static/current".format(name_no_ext))

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
