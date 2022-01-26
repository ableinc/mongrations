import zipfile, io, os, subprocess, shlex, shutil, sys
from setuptools.command.install import install
from time import sleep
import requests


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


if __name__ == '__main__':
    wrapper = InstallWrapper()
    wrapper.run()
