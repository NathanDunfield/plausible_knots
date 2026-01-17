long_description ="""\
This package provides a database of knots with at most 19 crossings
that are "plausibly slice" in that they have signature 0 and a
normalized Alexander polynomial that factors as f(t) f(t^-1) as in
Theorem 8.18 of [Lickorish, Intro to knot theory].
"""

import re, sys, subprocess, os, shutil, glob
import requests
from setuptools import setup, Command
from setuptools.command.build_py import build_py

# Even compressed, the CSV files that describe the knots/manifolds
# take up 400M.  The sqlite file is even larger at 1.1G. They are
# stored on GitHub using the Large File Storage system.  Here's code
# for fetching these.

pattern = ('version https://git-lfs.github.com/spec/v1\n'
           'oid sha256:([a-z0-9]+)\n'
           'size ([0-9]+)')


def get_lfs_file_url(user, repo, object_id, size):
    """
    Use the GitHub API to get URL to a LFS file.  The URL is dynamic and
    is good for an hour or so.
    """
    url = f'https://github.com/{user}/{repo}.git/info/lfs/objects/batch'
    body = {'operation': 'download',
            'transfer': ['basic'],
            'objects': [{'oid': object_id, 'size': size}]}
    headers = {'Accept':'application/vnd.git-lfs+json',
               'Content-Type': 'application/json'}
    response = requests.post(url, json=body, headers=headers)
    if response.status_code != 200:
        raise ConnectionError('Could not get download URL from GitHub')
    data = response.json()['objects'][0]
    assert data['oid'] == object_id
    return data['actions']['download']['href']


def download_as_file(url, path):
    """
    Based on https://stackoverflow.com/questions/16694907/
    """
    with requests.get(url, stream=True) as response:
        with open(path, 'wb') as file:
            shutil.copyfileobj(response.raw, file)


def fetch_if_needed(path):
    if os.path.getsize(path) < 1000:
        with open(path) as file:
            match = re.match(pattern, file.read())
            if match:
                oid, length = match.groups()
                length = int(length)
                url = get_lfs_file_url('NathanDunfield', 'plausible_knots', oid, length)
                os.rename(path, path + '.orig')
                print(f'Fetching data file {os.path.basename(path)}...',
                      end='', flush=True)
                download_as_file(url, path)
                if int(length) != os.path.getsize(path):
                    raise ConnectionError('Download was wrong size.')
                size = length/(1024**2)
                print(f' Successfully retrieved {size:.1f}M')

            
# --- end git lfs file stuff 


def check_call(args):
    try:
        subprocess.check_call(args)
    except subprocess.CalledProcessError:
        executable = args[0]
        command = [a for a in args if not a.startswith('-')][-1]
        raise RuntimeError(command + ' failed for ' + executable)


class Clean(Command):
    """
    Removes the usual build/dist/egg-info directories as well as the
    sqlite database files.
    """
    user_options = []
    def initialize_options(self):
        pass
    def finalize_options(self):
        pass
    def run(self):
        for dir in ['build', 'dist'] + glob.glob('*.egg-info'):
            if os.path.exists(dir):
                shutil.rmtree(dir)
        for file in glob.glob('manifold_src/*.sqlite'):
            os.remove(file)


class BuildPy(build_py):
    """
    Rebuilds the sqlite database files if needed.
    """
    def initialize_options(self):
        build_py.initialize_options(self)
        os.chdir('manifold_src')
        csv_source_files = glob.glob(
            os.path.join('original_manifold_sources', '*.csv*'))
        # When there are no csv files, we are in an sdist tarball
        if len(csv_source_files) == 0:
            fetch_if_needed('plausible_knots.sqlite')
        else:
            print('Rebuilding stale sqlite databases from csv sources if necessary...')
            check_call([sys.executable, 'make_sqlite_db.py'])
        os.chdir('..')


setup(
    packages = ['plausible_knots', 'plausible_knots/sqlite_files'],
    package_dir = {'plausible_knots':'python_src',
                   'plausible_knots/sqlite_files':'manifold_src'},
    package_data = {'plausible_knots/sqlite_files': ['plausible_knots.sqlite']},
    cmdclass = {'build_py': BuildPy,
                'clean': Clean,
    },
)
