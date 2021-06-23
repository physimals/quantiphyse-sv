"""
Setup script for quantiphyse-asl
"""
import os
import subprocess
import re
import io
import glob
import sys

from setuptools import setup
from setuptools import find_packages

import numpy

MODULE = 'quantiphyse_sv'

def get_filetext(rootdir, filename):
    """ Get the text of a local file """
    with io.open(os.path.join(rootdir, filename), encoding='utf-8') as f:
        return f.read()

def git_version():
    """ Get the full and python standardized version from Git tags (if possible) """
    try:
        # Full version includes the Git commit hash
        full_version = subprocess.check_output('git describe --dirty', shell=True).decode("utf-8").strip(" \n")

        # Python standardized version in form major.minor.patch.post<build>
        version_regex = re.compile(r"v?(\d+\.\d+(\.\d+)?(-\d+)?).*")
        match = version_regex.match(full_version)
        if match:
            std_version = match.group(1).replace("-", ".post")
        else:
            raise RuntimeError("Failed to parse version string %s" % full_version)
        return full_version, std_version
    except:
        # Any failure, return None. We may not be in a Git repo at all
        return None, None

def git_timestamp():
    """ Get the last commit timestamp from Git (if possible)"""
    try:
        return subprocess.check_output('git log -1 --format=%cd', shell=True).decode("utf-8").strip(" \n")
    except:
        # Any failure, return None. We may not be in a Git repo at all
        return None

def update_metadata(rootdir, version_str, timestamp_str):
    """ Update the version and timestamp metadata in the module _version.py file """
    with io.open(os.path.join(rootdir, MODULE, "_version.py"), "w", encoding='utf-8') as f:
        f.write("__version__ = '%s'\n" % version_str)
        f.write("__timestamp__ = '%s'\n" % timestamp_str)

def get_requirements(rootdir):
    """ Get a list of all entries in the requirements file """
    with io.open(os.path.join(rootdir, 'requirements.txt'), encoding='utf-8') as f:
        return [l.strip() for l in f.readlines()]

def get_version(rootdir):
    """ Get the current version number (and update it in the module _version.py file if necessary)"""
    version, timestamp = git_version()[1], git_timestamp()

    if version is not None and timestamp is not None:
        # We got the metadata from Git - update the version file
        update_metadata(rootdir, version, timestamp)
    else:
        # Could not get metadata from Git - use the version file if it exists
        with io.open(os.path.join(rootdir, MODULE, '_version.py'), encoding='utf-8') as f:
            md = f.read()
            match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", md, re.M)
            if match:
                version = match.group(1)
            else:
                version = "unknown"
    return version

def get_package_data(rootdir):
    """
    Get extra data files to install into the package, e.g. icons
    """
    return {
        MODULE : glob.glob("%s/*.png" % MODULE) + glob.glob("%s/*.svg" % MODULE)
    }

module_dir = os.path.abspath(os.path.dirname(__file__))

kwargs = {
    'name' : 'quantiphyse-sv',
    'version' : get_version(module_dir),
    'description' : 'Quantiphyse plugin for supervoxel clustering',
    'long_description' : get_filetext(module_dir, 'README.md'),
    'long_description_content_type' : 'text/markdown',
    'url' : 'https://quantiphyse.readthedocs.io/',
    'author' : 'Martin Craig',
    'author_email' : 'martin.craig@eng.ox.ac.uk',
    'license' : 'Apache-2.0',
    'setup_requires' : ['cython'],
    'install_requires' : get_requirements(module_dir),
    'packages' : find_packages(),
    'package_data' : get_package_data(module_dir),
    'include_package_data' : True,
    'entry_points' : {
        'quantiphyse_plugins' : [
            '%s = %s:QP_MANIFEST' % (MODULE, MODULE),
        ],
    },
    'classifiers' : [
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
        'License :: OSI Approved :: Apache Software License',
    ],
}

setup(**kwargs)
