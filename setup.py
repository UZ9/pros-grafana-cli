# setup.py for non-frozen builds

from setuptools import setup, find_packages
from install_requires import install_requires as install_reqs

setup(
    name='pros-grafana-cli',
    version=open('pip_version').read().strip(),
    packages=find_packages(),
    url='https://github.com/purduesigbots/pros-grafana-cli',
    license='MPL-2.0',
    author='Yerti',
    # author_email='',
    description='Command Line Interface for interacting with Grafana through a V5 Brain.',
    install_requires=install_reqs,
    entry_points={
        'console_scripts': [
            'prosgrafana=prosgrafana.cli.gui:gui',
        ]
    }
)
