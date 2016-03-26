import subprocess
from setuptools import setup
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))
readme = path.join(here, 'README.md')

# Convert the README to reStructuredText for PyPI if pandoc is available.
# Otherwise, just read it.
try:
    readme = subprocess.check_output(['pandoc', '-f', 'markdown', '-t', 'rst', readme]).decode('utf-8')
except:
    with open(readme, encoding='utf-8') as f:
        readme = f.read()

setup(
    name='perkele',
    version='0.1.0',

    license='WTFPL',
    description="A fully manual Let's Encrypt/ACME client",
    long_description=readme,
    url='https://github.com/schors/perkeLE',
    author="Veeti Paananen, Phil Kulin",
    author_email='schors@gmail.com',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3 :: Only',
    ],

    packages=['perkele'],
    install_requires=[
        'cryptography >= 1.0',
        'requests',
    ],

    entry_points={
        'console_scripts': [
            'perkele = perkele.cli:main',
        ],
    },
)
