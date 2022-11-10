from setuptools import setup
exec(open('ezfilelock/version.py').read())
setup(
    name='ezfilelock',
    version=__version__,
    packages=['ezfilelock'],
    url='https://github.com/jinmingyi1998/ezfilelock',
    license='MIT License',
    author='Mingyi Jin',
    author_email='jinmingyi1998@sina.cn',
    description='A simple cross-platform file lock'
)
