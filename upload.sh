rm -r dist/
python setup.py sdist bdist_wheel
# remove --repository-url argument to upload to real pipy
twine upload --repository-url https://test.pypi.org/legacy/ dist/*
