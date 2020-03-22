# remove compilation folder
rm -r dist/

# this requrieres packages "wheel" and "twine"
# install with pip
python setup.py test sdist bdist_wheel

# upload to pip
# remove --repository-url argument to upload to real pipy
twine upload --repository-url https://test.pypi.org/legacy/ dist/*
