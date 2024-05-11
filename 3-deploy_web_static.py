#!/usr/bin/python3

from fabric.api import local, run, put, env
from datetime import datetime
import os

# Define the hosts where the deployment will occur
env.hosts = ["54.157.191.51", "52.91.116.19"]


def do_pack():
    """Generates a.tgz archive"""
    local("mkdir -p versions")
    file_name = "versions/web_static_{}.tgz".format(
        datetime.now().strftime("%Y%m%d%H%M%S")
    )
    result = local("tar -cvzf {} web_static".format(file_name))
    if result.failed:
        return None
    return file_name


def do_deploy(archive_path):
    """
    Distributes an archive to web servers
    """
    if not os.path.isfile(archive_path):
        return False
    try:
        # Extract the file name from the archive_path
        file_name = archive_path.split("/")[-1]
        # Remove the extension from the file_name
        no_ext = file_name.split(".")[0]
        # Upload the archive to the /tmp/ directory of the web server
        put(archive_path, "/tmp/{}".format(file_name))
        # Uncompress the archive to the folder on the web server
        run("mkdir -p /data/web_static/releases/{}/".format(no_ext))
        run(
            "tar -xzf /tmp/{} -C /data/web_static/releases/{}/".format(
                file_name, no_ext
            )
        )
        # Delete the archive from the web server
        run("rm /tmp/{}".format(file_name))
        # Move the content to the final location
        run(
            "mv /data/web_static/releases/{}/web_static/* "
            "/data/web_static/releases/{}/".format(no_ext, no_ext)
        )
        run("rm -rf /data/web_static/releases/{}/web_static".format(no_ext))
        # Delete the symbolic link from the web server
        run("rm -rf /data/web_static/current")
        # Create a new the symbolic link on the web server
        run(
            "ln -s /data/web_static/releases/{}/ "
            "/data/web_static/current".format(no_ext)
        )
        print("New version deployed!")
        return True
    except Exception:
        return False


def deploy():
    """
    Deploys the web_static to the web servers
    """
    archive_path = do_pack()
    if not archive_path:
        return False
    return do_deploy(archive_path)


if __name__ == "__main__":
    deploy()
