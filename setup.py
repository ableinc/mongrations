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
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
