from setuptools import setup, find_packages

try:
    long_description = open("README.rst").read()
except IOError:
    long_description = ""

setup(
    name="arc-list-gen",
    version="1.0.0",
    description="Generate very specific lists of users and add them to a google group",
    url="https://github.com/bcomnes/arc-list-gen",
    license="MIT",
    author="Bret Comnes",
    packages=find_packages(),
    install_requires=[],
    long_description=long_description,
    zip_safe=True
)
