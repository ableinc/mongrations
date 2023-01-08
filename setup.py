import os.path as path
from setuptools import setup, find_packages

try:
    from mongrations.version import __version__
except ImportError:
    from mongrations import __version__


with open("README.md", "r") as fh:
    long_description = fh.read()



setup(
    name="mongrations",
    version=__version__,
    author="AbleInc - Jaylen Douglas",
    author_email="douglas.jaylen@gmail.com",
    description="Mongrations; a database independent migration and seeding tool for python.",
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
    install_requires=['Click', 'motor', 'pydotenvs', 'pymongo', 'PyMySQL', 'requests', 'psycopg[binary,pool]'],
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3 :: Only",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent"
    ],
)
