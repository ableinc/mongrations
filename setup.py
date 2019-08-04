import setuptools
from mongrations import __version__

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mongrations",
    version=__version__,
    author="AbleInc - Jaylen Douglas",
    author_email="douglas.jaylen@gmail.com",
    description="MongoDB Migrations for Python 3.5+",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ableinc/mongrations",
    keywords=['mongodb', 'migrations', 'python3', 'automation', 'database', 'json', 'nosql', 'python', 'database tool',
              'automation tool', 'open source'],
    packages=['mongrations'],
    entry_points='''
        [console_scripts]
        mongrations=mongrations.cli:mongrations
    ''',
    install_requires=[
          'click>=7.0',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
