# pylint: disable=C0111
from setuptools import setup

setup(
    name='unha',
    version='0.0.5',
    description='A library to simplify telnet connections to Cisco IOS devices',
    long_description=open('README.rst', 'r').read(),
    author='Renato Orgito',
    author_email='orgito@gmail.com',
    maintainer='Renato Orgito',
    maintainer_email='orgito@gmail.com',
    url='https://github.com/orgito/unha',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.6',
    ],
    keywords='unha network telnet automation',
    packages=['unha'],
    install_requires=[],
    python_requires='>=3.6',
    project_urls={
        'Bug Reports': 'https://github.com/orgito/unha/issues',
        'Source': 'https://github.com/orgito/unha',
    },
)
