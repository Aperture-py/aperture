"""Setup for Aperture distribution."""

from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

from aperture import __version__ as VERSION

setup(
    name='aperture',
    version=VERSION,
    description='An image re-sizing and compression tool',
    long_description=readme,
    url='https://github.com/Aperture-py/aperture',
    author='salvatorej1@wit.edu, kennedyd3@wit.edu, robbinsa@wit.edu',
    license=license,
    install_requires=['docopt', 'pillow==5.0.0'],
    entry_points={
        'console_scripts': ['aperture = aperture:main']
    },  # run the cli main function when aperture is run from the command line (i.e. '$ aperture')
    packages=find_packages(
        exclude=['docs', 'tests*']
    )  # prevent docs and tests from being installed on user's system as actual packages
)
