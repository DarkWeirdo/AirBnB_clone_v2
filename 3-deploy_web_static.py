#!/usr/bin/python3
"""
Fabric script that generates a .tgz archive from the contents of the web_static
folder of your AirBnB Clone repo, using the function do_pack.
"""
from fabric.api import local, put, run, env
from datetime import datetime
import os

env.hosts = ["54.157.191.51", "52.91.116.19"]


def do_pack():
    """
    Generates a .tgz archive from the contents of the web_static folder.
    """
    try:
        date_time = datetime.now().strftime("%Y%m%d%H%M%S")
        if not os.path.exists("versions"):
            local("mkdir versions")
        file_name = "versions/web_static_{}.tgz".format(date_time)
        local("tar -cvzf {} web_static".format(file_name))
        return file_name
    except Exception:
        return None


def do_deploy(archive_path):
    """
    Distributes an archive to the web servers.
    """
    if not os.path.exists(archive_path):
        return False
    try:
        file_name = archive_path.split("/")[-1]
        name = file_name.split(".")[0]
        path = "/data/web_static/releases/{}/".format(name)
        put(archive_path, "/tmp/")
        run("mkdir -p {}".format(path))
        run("tar -xzf /tmp/{} -C {}".format(file_name, path))
        run("rm /tmp/{}".format(file_name))
        run("mv {0}web_static/* {0}".format(path))
        run("rm -rf {}web_static".format(path))
        run("rm -rf /data/web_static/current")
        run("ln -s {} /data/web_static/current".format(path))
        print("New version deployed!")
        return True
    except Exception:
        return False


def deploy():
    """
    Creates and distributes an archive to the web servers.
    """
    archive_path = do_pack()
    if archive_path is None:
        return False
    return do_deploy(archive_path)
