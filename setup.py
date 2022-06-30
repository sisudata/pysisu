from setuptools import setup, find_packages

setup_info = dict(
    name='sisu_api',
    version='0.0.1',
    packages=find_packages(include=['sisu_api', 'sisu_api.*'])

)

setup(**setup_info)
