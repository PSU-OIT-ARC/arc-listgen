from setuptools import setup, find_packages

try:
    long_description = open("README.rst").read()
except IOError:
    long_description = ""

setup(
    name="listgen",
    version="1.0.0",
    description="Generate very specific lists of users and add them to a google group",
    url="https://github.com/bcomnes/arc-listgen",
    license="MIT",
    author="Bret Comnes",
    packages=find_packages(),
    install_requires=['ldap3'],
    test_suite='nose.collector',
    tests_require=['nose'],
    long_description=long_description,
    zip_safe=True,
    entry_points={
        'console_scripts': ['listgen=listgen:main'],
    }
)
