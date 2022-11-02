from setuptools import setup, find_packages

setup(
    name='NekPlot',
    version='0.2.0',
    packages=find_packages(include=['NekPlot', 'NekPlot.*']),
    install_requires=['matplotlib>=3.5.2','numpy>=1.22.4','pandas>=1.4.3']
)