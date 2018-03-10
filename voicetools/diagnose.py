# -*- coding: utf-8-*-
from __future__ import absolute_import
import os
import sys
import time
import socket
import subprocess
import pkgutil
import pip.req
import dingdangpath
if sys.version_info < (3, 3):
    from distutils.spawn import find_executable
else:
    from shutil import which as find_executable


def check_network_connection(server="www.baidu.com"):
    """
    Checks if dingdang can connect a network server.

    Arguments:
        server -- (optional) the server to connect with (Default:
                  "www.baidu.com")

    Returns:
        True or False
    """
    print("Checking network connection to server '%s'...", server)
    try:
        # see if we can resolve the host name -- tells us if there is
        # a DNS listening
        host = socket.gethostbyname(server)
        # connect to the host -- tells us if the host is actually
        # reachable
        socket.create_connection((host, 80), 2)
    except Exception:
        print("Network connection not working")
        return False
    else:
        print("Network connection working")
        return True


def check_executable(executable):
    """
    Checks if an executable exists in $PATH.

    Arguments:
        executable -- the name of the executable (e.g. "echo")

    Returns:
        True or False
    """
    print("Checking executable '%s'...", executable)
    executable_path = find_executable(executable)
    found = executable_path is not None
    if found:
        print("Executable '%s' found: '%s'", executable,
                     executable_path)
    else:
        print("Executable '%s' not found", executable)
    return found


def check_python_import(package_or_module):
    """
    Checks if a python package or module is importable.

    Arguments:
        package_or_module -- the package or module name to check

    Returns:
        True or False
    """
    # print("Checking python import '%s'...", package_or_module)
    loader = pkgutil.get_loader(package_or_module)
    found = loader is not None
    # if found:
    #     print("Python %s '%s' found: %r",
    #                  "package" if loader.is_package(package_or_module)
    #                  else "module", package_or_module, loader.get_filename())
    # else:
    #     print("Python import '%s' not found", package_or_module)
    return found


def get_pip_requirements(fname=os.path.join(dingdangpath.LIB_PATH,
                                            'requirements.txt')):
    """
    Gets the PIP requirements from a text file. If the files does not exists
    or is not readable, it returns None

    Arguments:
        fname -- (optional) the requirement text file (Default:
                 "client/requirements.txt")

    Returns:
        A list of pip requirement objects or None
    """
    if os.access(fname, os.R_OK):
        reqs = list(pip.req.parse_requirements(fname))
        print("Found %d PIP requirements in file '%s'", len(reqs),
                     fname)
        return reqs
    else:
        print("PIP requirements file '%s' not found or not readable",
                     fname)


def get_git_revision():
    """
    Gets the current git revision hash as hex string. If the git executable is
    missing or git is unable to get the revision, None is returned

    Returns:
        A hex string or None
    """
    if not check_executable('git'):
        print("'git' command not found, git revision not detectable")
        return None
    output = subprocess.check_output(['git', 'rev-parse', 'HEAD']).strip()
    if not output:
        print("Couldn't detect git revision (not a git repository?)")
        return None
    return output


def run():
    """
    Performs a series of checks against the system and writes the results to
    the logging system.

    Returns:
        The number of failed checks as integer
    """
    # Set loglevel of this module least to info
    # loglvl = logger.getEffectiveLevel()
    # if loglvl == logging.NOTSET or loglvl > logging.INFO:
    #     logger.setLevel(logging.INFO)

    print("Starting dingdang diagnostic at %s" % time.strftime("%c"))
    print("Git revision: %r", get_git_revision())

    failed_checks = 0

    if not check_network_connection():
        failed_checks += 1

    for executable in ['phonetisaurus-g2p', 'espeak', 'say']:
        if not check_executable(executable):
            print("Executable '%s' is missing in $PATH", executable)
            failed_checks += 1

    for req in get_pip_requirements():
        print("Checking PIP package '%s'...", req.name)
        if not req.check_if_exists():
            print("PIP package '%s' is missing", req.name)
            failed_checks += 1
        else:
            print("PIP package '%s' found", req.name)

    for fname in [os.path.join(dingdangpath.APP_PATH, os.pardir,
                               "phonetisaurus",
                               "g014b2b.fst")]:
        print("Checking file '%s'...", fname)
        if not os.access(fname, os.R_OK):
            print("File '%s' is missing", fname)
            failed_checks += 1
        else:
            print("File '%s' found", fname)

    if not failed_checks:
        print("All checks passed")
    else:
        print("%d checks failed" % failed_checks)

    return failed_checks


if __name__ == '__main__':
    # logging.basicConfig(stream=sys.stdout)
    # logger = logging.getLogger()
    # if '--debug' in sys.argv:
    #     logger.setLevel(logging.DEBUG)
    run()
