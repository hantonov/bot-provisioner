from setuptools import find_packages, setup

with open('bot/requirements.txt') as fp:
    install_requires = fp.read()

setup(
    name='bot',
    version='0.1.0',
    packages=find_packages(),
    zip_safe=False,
    install_requires=install_requires
)