# SLLib
A python library for reading SLG or SL2 files created by Lowrance fishfinders.
Only tested with python 3.6 and 3.7

Git Repostitory and homepage located at https://github.com/opensounder/python-sllib

# Installation
Using `pip`
```shell
pip install sllib
```

Cloning
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


## Examples
```shell
# this will create a file called `small.csv` in current directory
python ./examples/tocsv.py ./tests/sample-data-lowrance/Elite_4_Chirp/small.sl2

```