from setuptools import setup

__version__ = "undefined"  # if setup fails read it from _version.py and to please PyCharm
with open("README.md", 'r') as f:
    long_description = f.read()
exec(open('telegrame/_version.py').read())

setup(
    name='telegrame',
    version=__version__,
    description='telegrame',
    license="MIT",
    long_description=long_description,
    author='Egor Egorov',
    author_email='egigoka@gmail.com',
    url="https://www.github.com/egigoka/telegrame",
    packages=['telegrame'],  # same as name
    install_requires=['telebot==2.2.3'],
    extras_require={},
    include_package_data=True,
)
