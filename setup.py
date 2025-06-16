from setuptools import setup

from placards.__version__ import __version__


setup(
    name='placards',
    version=__version__,
    author='Ben Timby',
    author_email='btimby@gmail.com',
    description='A placards digital signage client for Linux in Python',
    long_description='Digital signage client using Pyppeteer to load resource in Chrome.',
    install_requires=['pyppeteer'],
    packages=['placards'],
    scripts=['bin/placards'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
    ],
)
