# SLLib
A python library for reading SLG or SL2 files created by Lowrance fishfinders.
Only tested with python 3.6 and 3.7

Git Repostitory and homepage located at https://github.com/opensounder/python-sllib

![example workflow](https://github.com/opensounder/python-sllib/actions/workflows/python-package.yml/badge.svg)

# Installation
Using `pip`
```shell
pip install sllib
```

Cloning from git
```
python3 setup.py install
```

# Usage
```
python3
>>> import sllib
>>> with open('somefile.sl2', 'rb) as f:
...    reader = sllib.Reader(f)
...    header = reader.header
...    print(header.format)
...    for frame in reader:
...        print(frame.gps_speed)

```
Or have a look at https://github.com/opensounder/jupyter-notebooks

## Examples
```shell
# this will create a file called `small.csv` in current directory
python ./examples/tocsv.py ./tests/sample-data-lowrance/Elite_4_Chirp/small.sl2

```


# Development
```shell
git clone https://github.com/opensounder/python-sllib

cd python-sllib
python3 -m venv venv
. venv/bin/activate
pip install -e .
pip install -r dev-requirements.txt

# then to test in for example python 3.9 
# change to what fits your installation
tox -e py39

# before committing please run lint and fix any issues
tox -e lint
```

# SLG information
Besides trial and error
- https://www.geotech1.com/forums/showthread.php?11159-Lowrance-MCC-saved-data-structure
- https://www.memotech.franken.de/FileFormats/Navico_SLG_Format.pdf