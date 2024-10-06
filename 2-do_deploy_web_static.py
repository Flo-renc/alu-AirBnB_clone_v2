#!/usr/bin/python3
""" Fabric script based on do_pack that distributes an archhive to websers
"""

from fabric.api import put, run, env
from os.path import exists
env.hosts = ['54.234.22.100','54.144.229.232']


def do_deploy(archive_path):
    """ distributes an archive to the web servers """
    if exists(archive_path) is False:
        return False
    try:
        fileName = archive_path.split("/")[-1]
        no_ext = fileName.split(".")[0]
        path = "/data/web_static/releases/"
        put(archive_path, '/tmp/')
        run('mkdir -p {}{}/'.format(path, no_ext))
        run('tar -xzf /tmp/{} -C {}{}/'.format(fileName, path, no_ext))
        run('rm/tmp/{}'.format(fileName))
        run('mv {0}{1}/web_static/* {0}{1}/'.format(path, no_ext))
        run('rm -rf {}{}/web_static'.format(path, no_ext))
        run('rm -rf /data/web_static/current')
        run('ln -s {}{}/ /data/web_static/current'.format(path, no_ext))
        return True
    except:
        return False
