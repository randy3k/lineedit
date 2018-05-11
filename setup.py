import os
import re
from setuptools import setup, find_packages


def get_long_description():
    with open('README.md', 'rb') as f:
        desc = f.read().decode('utf-8')

    return desc


def get_version(package):
    """
    Return package version as listed in `__version__` in `__init__.py`.
    """
    path = os.path.join(os.path.dirname(__file__), package, '__init__.py')
    with open(path, 'rb') as f:
        init_py = f.read().decode('utf-8')
    return re.search("__version__ = ['\"]([^'\"]+)['\"]", init_py).group(1)


setup(
    name='lineedit',
    author='Randy Lai',
    version=get_version("lineedit"),
    url='https://github.com/randy3k/lineedit',
    description='An readline library based on prompt_toolkit which supports multiple modes',
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    packages=find_packages('.'),
    install_requires=[
        'pygments',
        'six',
        'wcwidth'
    ]
)
