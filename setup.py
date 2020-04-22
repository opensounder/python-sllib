from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='sllib',
    python_requires='>3.6.0',
    version='0.0.1',
    description='Library for reading SLG or SL2 files created by Lowrance fishfinders',
    url='http://github.com/opensounder/python-sllib',
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    author='Peter Magnusson',
    author_email='peter@kmpm.se',
    license='MIT',
    packages=['sllib'],
    install_requires=[],
    test_suite='tests',
    zip_safe=False)
