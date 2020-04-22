# Publishing
Based upon https://packaging.python.org/tutorials/packaging-projects/
```shell
pip install --upgrade setuptools wheel twine

# generate archives
python .\setup.py sdist bdist_wheel

# keyring gets installed with twine
keyring set https://test.pypi.org/legacy/ your-username

# test upload
twine upload --repository testpypi dist/*

# in a fresh virtualenv test to install
pip install --index-url https://test.pypi.org/simple/ --no-deps sllib-YOUR-USERNAME-HERE
```


## Publish in Production 
```shell
keyring set https://upload.pypi.org/legacy/ your-username
twine upload dist/*
```