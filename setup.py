from setuptools import setup, find_packages

setup(
    name='sisu_api',
    version='0.0.1',
    packages=find_packages(include=['sisu_api', 'sisu_api.*']),
    install_requires=[
        'betterproto>=2.0.0b4',
    ],
)
