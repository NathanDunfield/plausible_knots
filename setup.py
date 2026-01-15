long_description ="""\
This package provides a database of knots with at most 19 crossings
that are "plausibly slice" in that they have signature 0 and a
normalized Alexander polynomial that factors as f(t) f(t^-1) as in
Theorem 8.18 of [Lickorish, Intro to knot theory].
"""

import re, sys, subprocess, os, shutil, glob, sysconfig
from setuptools import setup, Command
from setuptools.command.build_py import build_py

sqlite_files = ['plausible_knots.sqlite']


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
        if len(csv_source_files) != 0:
            if self.force:
                for file in glob.glob('*.sqlite'):
                    os.remove(file)
            print('Rebuilding stale sqlite databases from csv sources if necessary...')
            check_call([sys.executable, 'make_sqlite_db.py'])
        os.chdir('..')


setup(
    packages = ['plausible_knots', 'plausible_knots/sqlite_files'],
    package_dir = {'plausible_knots':'python_src',
                   'plausible_knots/sqlite_files':'manifold_src'},
    package_data = {'plausible_knots/sqlite_files': sqlite_files},
    zip_safe = False,
    cmdclass = {'build_py': BuildPy,
                'clean': Clean,
    },
)
