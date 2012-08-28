from setuptools import setup, find_packages

VERSION = '0.0.1-dev'

LONG_DESCRIPTION = open('README.rst').read()

setup(name='appcontainers',
    version=VERSION,
    description="dploy's library",
    long_description=LONG_DESCRIPTION,
    keywords='',
    author='Reuven V. Gonzales',
    author_email='reuven@tobetter.us',
    url="https://github.com/ravenac95/appcontainers",
    license='MIT',
    platforms='*nix',
    packages=find_packages(exclude=['ez_setup', 'examples', 'prototyping', 'tests']),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'lxc4u',
        'tempita',
        'ipaddr',
        'ZODB3',
    ],
    entry_points={},
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Operating System :: POSIX',
    ],
)
