#!/usr/bin/python3
"""
Fabric script that distributes an archive to web servers
"""
from fabric.api import env, put, run
from os.path import isfile

env.hosts = ["54.157.191.51", "52.91.116.19"]


def do_deploy(archive_path):
    """
    Distributes an archive to web servers
    """
    if not isfile(archive_path):
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
