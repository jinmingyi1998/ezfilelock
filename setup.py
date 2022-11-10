from setuptools import setup
from pathlib import Path

exec(open('ezfilelock/version.py').read())
long_description = Path("README.md").read_text()
setup(
    name='ezfilelock',
    version=__version__,
    packages=['ezfilelock'],
    url='https://github.com/jinmingyi1998/ezfilelock',
    license='MIT License',
    author='Mingyi Jin',
    author_email='jinmingyi1998@sina.cn',
    description='A simple cross-platform file lock',
    long_description=long_description,
    long_description_content_type='text/markdown'
)
