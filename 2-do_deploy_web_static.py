#!/usr/bin/python3
from fabric.api import env, put, run
from os.path import exists

env.hosts = ['ubuntu@52.91.116.19', 'ubuntu@54.157.191.51']

def do_deploy(archive_path):
    """
    Distributes an archive to web servers
    """
    if not exists(archive_path):
        return False

    try:
        # Upload the archive to the /tmp/ directory of the web server
        put(archive_path, "/tmp/")
        # Get the file name without extension
        file_name = archive_path.split("/")[-1]
        name = file_name.split(".")[0]
        # Uncompress the archive to the folder on the web server
        run("mkdir -p /data/web_static/releases/{}/".format(name))
        run("tar -xzf /tmp/{} -C /data/web_static/releases/{}/".format(file_name, name))
        # Delete the archive from the web server
        run("rm /tmp/{}".format(file_name))
        # Delete the symbolic link from the web server
        run("rm -rf /data/web_static/current")
        # Create a new the symbolic link on the web server
        run("ln -s /data/web_static/releases/{}/ /data/web_static/current".format(name))
        return True
    except:
        return False
