try:
    from setuptools import setuptools
except ImportError:
    from distultils.core import setuptools

config = {
    'description': 'A sudoku game using pygames',
    'author': 'Olivier Moreau',
    'url': 'URL',
    'download_url': '',
    'author_email': 'oliviermoreau676@gmail.com',
    'version': '0.1',
    'install_requires': ['nose'],
    'packages': ['NAME'],
    'scripts': [],
    'name': 'projectname'
}

setup(**config, install_requires=['pygame'])
