import zipfile, io, os, subprocess, shlex, shutil, sys
import os.path as path
from setuptools import setup, find_packages
from setuptools.command.install import install
from time import sleep
import requests
try:
    from mongrations.version import __version__
except ImportError:
    from mongrations import __version__


with open("README.md", "r") as fh:
    long_description = fh.read()


class InstallWrapper(install):
    psycopg2_url = 'https://github.com/psycopg/psycopg2/archive/master.zip'
        
    def run(self):
        self.install_postgres()
        install.run(self)
    
    def install_postgres(self):
        # Install Postgres DB Python Tool
        save_dir = os.path.join(str(os.getcwd()) + '/temp/')
        print('You will be prompted to install Postgres dependencies. One moment...')
        sleep(3)
        choice = input('Install psycopg2 from source? (y/n) ')
        if choice.lower() == 'y':
            path_ = input('path to pg_config (default: current directory) > ')
            if path_ == '':
                path_ = os.getcwd()
            sys.path.append(path_)
            try:
                # Make Directory and Download Driver
                os.makedirs(save_dir)
                content = requests.get(self.psycopg2_url).content
                file = zipfile.ZipFile(io.BytesIO(content))
                file.extractall(save_dir)
                print('Installing psycopg2 from source...')
                # Install Driver
                for command in ['cd temp/psycopg2-master && python3 setup.py build && python3 setup.py install',
                                'python3 -c "import psycopg2"']:
                    proc = subprocess.Popen(shlex.split(command), stdout=subprocess.PIPE)
                    for line in io.TextIOWrapper(proc.stdout, encoding='utf-8'):
                        print(line)
            except zipfile.BadZipFile:
                pass
            except subprocess.CalledProcessError:
                print(
                    f'Fatal error installing psycopg2. Manually install by following '
                    f'this: https://github.com/psycopg/psycopg2')
            finally:
                print('Installation complete.')
                shutil.rmtree(save_dir, True)


setup(
    name="mongrations",
    version=__version__,
    author="AbleInc - Jaylen Douglas",
    author_email="douglas.jaylen@gmail.com",
    description="Mongrations; a database migration tool for Python 3.6 and above.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ableinc/mongrations",
    keywords=['migrations', 'python3', 'automation', 'database', 'json', 'nosql', 'python', 'database tool',
              'automation tool', 'open source', 'mongodb', 'mysql', 'postgres', 'sql'],
    packages=find_packages(),
    include_package_data=True,
    package_data={
      'mongrations': ['mongrations/data/template.txt']
    },
    data_files=[
        ('/mongrations/data', [path.join('mongrations/data', 'template.txt')])
    ],
    entry_points='''
        [console_scripts]
        mongrations=mongrations.cli:cli
    ''',
    install_requires=['Click', 'motor', 'pydotenvs', 'pymongo', 'PyMySQL', 'requests'],
    cmdclass={'develop': InstallWrapper},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
