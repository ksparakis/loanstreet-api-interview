from setuptools import setup

setup(
    # Needed to silence warnings (and to be a worthwhile package)
    name='Pyless',
    url='git@gitlab.com:pyless/pyless-py3.git',
    author='Konstantinos Sparakis',
    author_email='ksparakis@gmail.com',
    # Needed to actually package something
    packages=['pyless'],
    # Needed for dependencies
    install_requires=['boto3', 'peewee', 'enum34'],
    # *strongly* suggested for sharing
    version='0.1',
    # The license can be anything you like
    license='MIT',
    description='for interview with loanstreet',
    # long_description=open('README.txt').read(),
)
