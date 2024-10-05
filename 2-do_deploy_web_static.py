#!/usr/bin/python3
"""
A Fabric script that distributes an archive to the 
web servers using the function do_deploy

"""

from fabric.api import env, put, run
import os

env.hosts = ['54.234.22.100', '54.234.22.100']


def do_deploy(archive_path):
    """This function distributes an archive to the web servers web_01 and web_02 """
    
    if not os.path.exists(archive_path):
        return False
    try:
        archive_file = archive_path.split("/")[-1]
        archive_name = archive_dile_path.split(".")[0]

        put(archive_path, "/tmp/{}".format(archive_file))

        release_dir = "/data/web_static/release/{}/".format(archive_name)
        run("sudo mkidr -p {}".format(release_dir))

        run("sudo tar -xzf /tmp/{} -C {}".format(archive_file, release_dir))

        run("sudo rm /tmp/{}".format(archive_file))
        run("sudo mv {0}web_static/* {0}".format(release_dir))

        run("sudo rm -rf {}/web_static".format(release_dir))
        run("sudo ln -s {} /data/web_static/current".format(release_dir))

        print("New version deployed!")
        return True

    except Exception as e:
        print(f"Error occurred: {e}")
        return False
