#!/usr/bin/python3
"""Fabric script that generates a .tgz archive from the web_static"""
from fabric.api import local
from datetime import datetime


def do_pack():
    """Generates a .tgz archive"""
    local("mkdir -p versions")
    file_name = "versions/web_static_{}.tgz".format(
        datetime.now().strftime("%Y%m%d%H%M%S")
    )
    result = local("tar -cvzf {} web_static".format(file_name))
    if result.failed:
        return None
    return file_name
