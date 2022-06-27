from setuptools import setup, find_packages

setup(
    name='pros-grafana-cli',
    version=open('pip_version').read().strip(),
    packages=find_packages(),
    url='https://github.com/UZ9/pros-grafana-cli',
    license='MPL-2.0',
    author='Yerti',
    description='Command Line Interface for interacting with Grafana through a V5 Brain.',
    install_requires=[
        "click>=6,<7",
        "pros-cli",
        "setuptools~=56.0.0"
    ],
    entry_points={
        'console_scripts': [
            'prosgrafana=prosgrafana.cli.gui:gui',
        ]
    }
)
