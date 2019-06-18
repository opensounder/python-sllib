from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='sllib',
    python_requires='>3.6.0',
    version='0.0.1',
    description='some kind of asyncio library for GoPro',
    url='http://github.com/opensounder/python-sllib',
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
    ],
    author='Peter Magnusson',
    author_email='peter@birchroad.net',
    license='MIT',
    packages=['sllib'],
    install_requires=[],
    test_suite='tests',
    zip_safe=False)
