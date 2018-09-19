import io
import os
import sys
from shutil import rmtree

from setuptools import Command, find_packages, setup

import migrator

HERE = os.path.abspath(os.path.dirname(__file__))

# Package meta-data.
NAME = 'redis-migrate'
DESCRIPTION = 'A simple command line tool for redis data migration'
URL = 'https://github.com/mingrammer/redis-migrate'
EMAIL = 'mingrammer@gmail.com'

# What packages are required for this module to be execuøted?
REQUIRED = []
with io.open(os.path.join(HERE, 'requirements.txt'), encoding='utf-8') as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        REQUIRED.append(line)

# Import the README and use it as the long-description.
# Note: this will only work if 'README.rst' is present in your MANIFEST.in file!
with io.open(os.path.join(HERE, 'README.md'), encoding='utf-8') as f:
    long_description = '\n' + f.read()


class PublishCommand(Command):
    """Support setup.py publish."""

    description = 'Build and publish the package.'
    user_options = []

    @staticmethod
    def status(s):
        """Prints things in bold."""
        print('\033[1m{0}\033[0m'.format(s))

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            self.status('Removing previous builds…')
            rmtree(os.path.join(HERE, 'dist'))
        except OSError:
            pass

        self.status('Building Source and Wheel (universal) distribution…')
        os.system(
            '{0} setup.py sdist bdist_wheel --universal'.format(sys.executable))

        self.status('Uploading the package to PyPi via Twine…')
        os.system('twine upload dist/*')

        sys.exit()


setup(
    name=NAME,
    version=migrator.__version__,
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type='text/markdown',
    author=migrator.__author__,
    author_email=EMAIL,
    url=URL,
    keywords='redis migrate',
    packages=find_packages(),
    entry_points={
        'console_scripts': ['redis-migrate=migrator.main:main'],
    },
    install_requires=REQUIRED,
    include_package_data=True,
    license=migrator.__license__,
    python_requires='>=3',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Topic :: Terminals',

    ],
    # $ setup.py publish support.
    cmdclass={
        'publish': PublishCommand,
    },
)
