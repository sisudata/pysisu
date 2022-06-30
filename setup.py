from setuptools import setup, find_packages

setup(
    name='pysisu',
    version='0.0.1',
    packages=find_packages(include=['pysisu', 'pysisu.*']),
    install_requires=[
        'betterproto>=2.0.0b4',
    ],
)
