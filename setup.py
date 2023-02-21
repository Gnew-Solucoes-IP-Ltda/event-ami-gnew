import os
from setuptools import setup


lib_folder = os.path.dirname(os.path.realpath(__file__))
requirement_path = lib_folder + '/requirements.txt'
install_requires = []

# Obtain list of requirements
if os.path.isfile(requirement_path):
    with open(requirement_path) as f:
        install_requires = f.read().splitlines()

# Obtain readme text for long description
with open("README.md", "r") as arq:
    readme = arq.read()

setup(
    name='event-ami-asterisk',
    version='0.1.0',
    license='MIT License',
    author='Tatianno Alves',
    long_description=readme,
    long_description_content_type="text/markdown",
    author_email='tferreiraalves@gmail.com',
    keywords='asterisk ami gnew',
    description=u'Manager for Asterisk events received from AMI',
    packages=['event_ami_gnew'],
    install_requires=install_requires,
)